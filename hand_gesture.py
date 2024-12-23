import cv2
from mediapipe import solutions as mp_solutions
import pyttsx3

mp_hands = mp_solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp_solutions.drawing_utils
engine = pyttsx3.init()

gesture_mapping = {
    "thumbs_up": "Yes",
    "palm_open": "Hello",
    "fist_closed": "No",
    "peace_sign": "Peace",
    "pointing": "Look here",
    "ok_sign": "Okay",
}

def classify_hand_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]
    thumb_ip = landmarks[3]

    if thumb_tip.y < thumb_ip.y and all(finger.y > thumb_ip.y for finger in [index_tip, middle_tip, ring_tip, pinky_tip]):
        return "thumbs_up"
    elif all(finger.y < thumb_tip.y for finger in [index_tip, middle_tip, ring_tip, pinky_tip]):
        return "palm_open"
    elif all(finger.y > thumb_tip.y for finger in [index_tip, middle_tip, ring_tip, pinky_tip]):
        return "fist_closed"
    elif index_tip.y < thumb_tip.y and middle_tip.y < thumb_tip.y and ring_tip.y > thumb_tip.y and pinky_tip.y > thumb_tip.y:
        return "peace_sign"
    elif index_tip.y < thumb_tip.y and all(finger.y > thumb_tip.y for finger in [middle_tip, ring_tip, pinky_tip]):
        return "pointing"
    elif abs(thumb_tip.x - index_tip.x) < 0.03 and abs(thumb_tip.y - index_tip.y) < 0.03:
        return "ok_sign"
    else:
        return "unknown"

def main():
    cap = cv2.VideoCapture(0) 


    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_count = 0  # Counter to process every other frame

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        
        frame = cv2.resize(frame, (640, 480))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if frame_count % 2 == 0:  # Skip every other frame
            result = hands.process(rgb_frame)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
               
                    gesture = classify_hand_gesture(hand_landmarks.landmark)
                    text = gesture_mapping.get(gesture, "Gesture not recognized")

                   
                    if gesture != "unknown":
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                        
                        engine.say(text)
                        engine.runAndWait()

        frame_count += 1  # Increment frame counter

        cv2.imshow("Hand Gesture Communicator", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
