import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

threshold_x = 0.01
threshold_y = 0.01
prev_x, prev_y = 0, 0
last_click_time = time.time()
double_clicked = False

class Controller:
    prev_hand = None
    double_clicked = False
    hand_Landmarks = None
    screen_width, screen_height = pyautogui.size()

    @staticmethod
    def update_fingers_status():
        Controller.index_finger_up = Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[5].y
        Controller.thumb_up = Controller.hand_Landmarks.landmark[4].y < Controller.hand_Landmarks.landmark[2].y
        Controller.pinky_up = Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[17].y
        Controller.all_fingers_up = all(Controller.hand_Landmarks.landmark[i].y < Controller.hand_Landmarks.landmark[i - 2].y
                                        for i in [8, 12, 16, 20])
        Controller.all_fingers_down = all(Controller.hand_Landmarks.landmark[i].y > Controller.hand_Landmarks.landmark[i - 2].y
                                          for i in [8, 12, 16, 20])

    @staticmethod
    def get_position(hand_x_position, hand_y_position):
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x_position * Controller.screen_width)
        current_y = int(hand_y_position * Controller.screen_height)

        ratio = 1
        Controller.prev_hand = (current_x, current_y) if Controller.prev_hand is None else Controller.prev_hand
        delta_x = current_x - Controller.prev_hand[0]
        delta_y = current_y - Controller.prev_hand[1]

        Controller.prev_hand = [current_x, current_y]
        current_x, current_y = old_x + delta_x * ratio, old_y + delta_y * ratio

        threshold = 5
        if current_x < threshold:
            current_x = threshold
        elif current_x > Controller.screen_width - threshold:
            current_x = Controller.screen_width - threshold
        if current_y < threshold:
            current_y = threshold
        elif current_y > Controller.screen_height - threshold:
            current_y = Controller.screen_height - threshold

        return (current_x, current_y)

    @staticmethod
    def cursor_moving():
        point = 9
        current_x, current_y = Controller.hand_Landmarks.landmark[point].x, Controller.hand_Landmarks.landmark[point].y
        x, y = Controller.get_position(current_x, current_y)
        cursor_freezed = Controller.all_fingers_up and Controller.thumb_up
        if not cursor_freezed:
            pyautogui.moveTo(x, y, duration=0)

    @staticmethod
    def detect_actions():
        if Controller.index_finger_up and not Controller.thumb_up and not Controller.pinky_up:
            pyautogui.moveRel(0, -20)
        elif Controller.thumb_up and not Controller.index_finger_up and not Controller.pinky_up:
            pyautogui.moveRel(-20, 0) 
        elif Controller.pinky_up and not Controller.index_finger_up and not Controller.thumb_up:
            pyautogui.moveRel(20, 0)
        elif not Controller.index_finger_up and Controller.thumb_up and Controller.pinky_up:
            pyautogui.moveRel(0, 20) 

        if Controller.all_fingers_up:
            pyautogui.doubleClick()
            Controller.double_clicked = True

        if Controller.all_fingers_down:
            pyautogui.hotkey('alt', 'f4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            Controller.hand_Landmarks = hand_landmarks
            Controller.update_fingers_status()
            Controller.cursor_moving()
            Controller.detect_actions()

    cv2.imshow('Gesture Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
