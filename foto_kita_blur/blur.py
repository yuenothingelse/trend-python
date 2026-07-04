import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

def is_peace(hand_landmarks):

    lm = hand_landmarks.landmark

    index_up = lm[8].y < lm[6].y
    middle_up = lm[12].y < lm[10].y
    ring_down = lm[16].y > lm[14].y
    pinky_down = lm[20].y > lm[18].y

    return (
        index_up and
        middle_up and
        ring_down and
        pinky_down
    )

def is_rock(hand_landmarks):

    lm = hand_landmarks.landmark

    index_up = lm[8].y < lm[6].y
    middle_down = lm[12].y > lm[10].y
    ring_down = lm[16].y > lm[14].y
    pinky_up = lm[20].y < lm[18].y

    return (
        index_up and
        middle_down and
        ring_down and
        pinky_up
    )

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera tidak dapat dibuka")
    exit()

print("=======================================")
print("✌️ Peace atau 🤘 Rock = Blur 5 Detik")
print("ESC = Keluar")
print("=======================================")

cap.release()
cv2.destroyAllWindows()
