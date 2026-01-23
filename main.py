import cv2 
import mediapipe as mp 
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

meme_image = cv2.imread("meme/staring.png")
if meme_image is None:
    print("Error: Could not load meme image")
    exit()

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')

options = vision.HandLandmarkerOptions(
    base_options = base_options,
    num_hands = 2,
    running_mode = vision.RunningMode.VIDEO,
    min_hand_detection_confidence = 0.6,
    min_tracking_confidence = 0.6)

landmarker = vision.HandLandmarker.create_from_options(options)

# Try camera index 1 if 0 doesn't work
cap = cv2.VideoCapture(1)
timestamp = 0

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

print("Camera opened successfully!")
print(f"Camera width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
print(f"Camera height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

while cap.isOpened():
    valid, frame = cap.read()

    if not valid:
        print("Warning: Could not read frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(
        image_format = mp.ImageFormat.SRGB,
        data = rgb_frame
    )
    
    result = landmarker.detect_for_video(mp_image, timestamp)
    timestamp += 1
    gesture_text = ""
    
    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            
            index_tip = hand[8]
            index_pip = hand[6]
            middle_tip = hand[12]
            middle_pip = hand[10]
            ring_tip = hand[16]
            ring_pip = hand[14]
            pinky_tip = hand[20]
            pinky_pip = hand[18]


            index_extended = index_tip.y < index_pip.y
            middle_folded = middle_tip.y > middle_pip.y
            ring_folded = ring_tip.y > ring_pip.y
            pinky_folded = pinky_tip.y > pinky_pip.y

            if index_extended and middle_folded and ring_folded and pinky_folded:
                gesture_text = "POINTING!"
                meme_image = cv2.imread("meme/pointing.png")
            else:
                guesture_text = ""
                meme_image = cv2.imread("meme/staring.png")    

            for lm in hand:
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
    else:
        meme_image = cv2.imread("meme/staring.png")
        
    frame_height, frame_width = frame.shape[:2]
    meme_resized = cv2.resize(meme_image, (frame_width, frame_height))
    combined = np.hstack([meme_resized, frame])
    
    cv2.imshow('Think Monke', combined)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
landmarker.close()

 