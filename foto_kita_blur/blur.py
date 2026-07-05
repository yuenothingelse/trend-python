import cv2
import mediapipe as mp
import time

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Gesture Peace
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

# Gesture Rock
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

blur_duration = 1.5 

blur_until = 0

while True:

    success, frame = cap.read()

    if not success:
        print("Gagal membaca kamera")
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    gesture_detected = False

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            if time.time() >= blur_until:
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

            if is_peace(hand_landmarks) or is_rock(hand_landmarks):
                gesture_detected = True

    if gesture_detected:
        blur_until = time.time() + blur_duration

    if time.time() < blur_until:

        frame = cv2.GaussianBlur(
            frame,
            (99, 99),
            30
        )

        remaining = int(blur_until - time.time()) + 1

        cv2.putText(
            frame,
            f"PRIVACY MODE ({remaining})",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

    else:

        cv2.putText(
            frame,
            "NORMAL MODE",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

    cv2.imshow("Gesture Privacy Mode", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
