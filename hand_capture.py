import cv2

# import mediapipe.python.solutions.hands as mp_hands
import mediapipe as mp
import mediapipe.python.solutions.drawing_utils as mp_drawing
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if not ret:
        break
    image_rgb = cv2.cvtColor(
        frame, cv2.COLOR_BGR2RGB
    )  # taking every frame and changing it to rgb
    results = hands.process(image_rgb)  # process the frame
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
        index_finger_y = hand_landmark.landmark[
            mp_hands.HandLandmark.INDEX_FINGER_TIP
        ].y
        thumb_y = hand_landmark.landmark[mp_hands.HandLandmark.THUMB_TIP].y
        mid_y = hand_landmark.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
        lambdaDis = index_finger_y - thumb_y
        if lambdaDis < -0.14:
            hand_gesture = "volumeup"

        elif lambdaDis > 0.08:
            hand_gesture = "volumedown"
        # elif mid_y>0.4 and lambdaDis >0.01 and lambdaDis<0.09:
        #     hand_gesture="playpause"

        else:
            hand_gesture = "other"

        print("dis between in to thumb", index_finger_y - thumb_y)
        # print("midy",mid_y)
        pyautogui.press(hand_gesture)

        cv2.imshow("Hand Gesture", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
