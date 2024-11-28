import pyautogui
class Controller:
    prev_hand = None
    right_clicked = False
    left_clicked = False
    double_clicked = False
    dragging = False
    hand_Landmarks = None
    little_finger_down = None
    little_finger_up = None
    index_finger_down = None
    index_finger_up = None
    middle_finger_down = None
    middle_finger_up = None
    ring_finger_down = None
    ring_finger_up = None
    Thump_finger_down = None 
    Thump_finger_up = None
    all_fingers_down = None
    all_fingers_up = None
    index_finger_within_Thumb_finger = None
    middle_finger_within_Thumb_finger = None
    little_finger_within_Thumb_finger = None
    ring_finger_within_Thumb_finger = None
    screen_width, screen_height = pyautogui.size()


    def update_fingers_status():
        Controller.little_finger_down = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[17].y
        Controller.little_finger_up = Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[17].y
        Controller.index_finger_down = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[5].y
        Controller.index_finger_up = Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[5].y
        Controller.middle_finger_down = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[9].y
        Controller.middle_finger_up = Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[9].y
        Controller.ring_finger_down = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[13].y
        Controller.ring_finger_up = Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[13].y
        Controller.Thump_finger_down = Controller.hand_Landmarks.landmark[4].y > Controller.hand_Landmarks.landmark[13].y
        Controller.Thump_finger_up = Controller.hand_Landmarks.landmark[4].y < Controller.hand_Landmarks.landmark[13].y
        Controller.all_fingers_down = Controller.index_finger_down and Controller.middle_finger_down and Controller.ring_finger_down and Controller.little_finger_down
        Controller.all_fingers_up = Controller.index_finger_up and Controller.middle_finger_up and Controller.ring_finger_up and Controller.little_finger_up
        Controller.index_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[2].y
        Controller.middle_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[2].y
        Controller.little_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[2].y
        Controller.ring_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[2].y
    
    def get_position(hand_x_position, hand_y_position):
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x_position * Controller.screen_width)
        current_y = int(hand_y_position * Controller.screen_height)

        ratio = 1
        Controller.prev_hand = (current_x, current_y) if Controller.prev_hand is None else Controller.prev_hand
        delta_x = current_x - Controller.prev_hand[0]
        delta_y = current_y - Controller.prev_hand[1]
        
        Controller.prev_hand = [current_x, current_y]
        current_x , current_y = old_x + delta_x * ratio , old_y + delta_y * ratio

        threshold = 5
        if current_x < threshold:
            current_x = threshold
        elif current_x > Controller.screen_width - threshold:
            current_x = Controller.screen_width - threshold
        if current_y < threshold:
            current_y = threshold
        elif current_y > Controller.screen_height - threshold:
            current_y = Controller.screen_height - threshold

        return (current_x,current_y)
        
    def cursor_moving():
        point = 9
        current_x, current_y = Controller.hand_Landmarks.landmark[point].x ,Controller.hand_Landmarks.landmark[point].y
        x, y = Controller.get_position(current_x, current_y)
        cursor_freezed = Controller.all_fingers_up and Controller.Thump_finger_down
        if not cursor_freezed:
            pyautogui.moveTo(x, y, duration = 0)
    
    def detect_scrolling():
        scrolling_up =  Controller.little_finger_up and Controller.index_finger_down and Controller.middle_finger_down and Controller.ring_finger_down
        if scrolling_up:
            pyautogui.scroll(120)
            print("Scrolling UP")

        scrolling_down = Controller.index_finger_up and Controller.middle_finger_down and Controller.ring_finger_down and Controller.little_finger_down
        if scrolling_down:
            pyautogui.scroll(-120)
            print("Scrolling DOWN")
    

    def detect_clicking():        
        if Controller.all_fingers_up:
            pyautogui.doubleClick()
            Controller.double_clicked = True    
        else:
            Controller.double_clicked = False
            
        if Controller.all_fingers_down:
            pyautogui.hotkey('alt', 'f4')
            print("closing")
            
    