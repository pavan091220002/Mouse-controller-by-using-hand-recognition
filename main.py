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

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the y-coordinates of the finger tips and MCP joints
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
            pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y

            # Check if only the index finger is up
            if index_tip < index_mcp and thumb_tip > thumb_mcp and pinky_tip > pinky_mcp:
                pyautogui.moveRel(0, 20)  # Move cursor up

            # Check if only the thumb is up
            elif thumb_tip < thumb_mcp and index_tip > index_mcp and pinky_tip > pinky_mcp:
                pyautogui.moveRel(-20, 0)  # Move cursor left

            # Check if only the pinky is up
            elif pinky_tip < pinky_mcp and index_tip > index_mcp and thumb_tip > thumb_mcp:
                pyautogui.moveRel(20, 0)  # Move cursor right

            # Check if both index finger and thumb are down
            elif index_tip < index_mcp and thumb_tip < thumb_mcp:
                pyautogui.moveRel(0, -20)

            # Check if the hand is open
            is_open = all(hand_landmarks.landmark[i].y < hand_landmarks.landmark[i - 2].y
                          for i in [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
                                    mp_hands.HandLandmark.PINKY_TIP])

            if is_open:
                pyautogui.doubleClick()
                double_clicked = True

            # Check if the hand is closed
            is_closed = all(hand_landmarks.landmark[i].y > hand_landmarks.landmark[i - 2].y
                            for i in [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                      mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP,
                                      mp_hands.HandLandmark.PINKY_TIP])
            if is_closed:
                print("1")
                pyautogui.hotkey('alt', 'f4')

    cv2.imshow('Gesture Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
