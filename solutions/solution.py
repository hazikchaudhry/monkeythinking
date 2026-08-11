import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

ASSETS = Path(__file__).resolve().parent.parent

# Load the default meme image
meme_image = cv2.imread(str(ASSETS / "meme" / "staring.png"))
if meme_image is None:
    print("Error: Could not load meme image")
    exit()

# Setup hand detection model
base_options = python.BaseOptions(model_asset_path=str(ASSETS / "models" / "hand_landmarker.task"))

options = vision.HandLandmarkerOptions(
    base_options = base_options,
    num_hands = 2,
    running_mode = vision.RunningMode.VIDEO,
    min_hand_detection_confidence = 0.6,
    min_tracking_confidence = 0.6)

landmarker = vision.HandLandmarker.create_from_options(options)

# Open camera (index 0 is usually the built-in webcam; try a few if yours differs)
def open_camera(max_index=3):
    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"Camera opened at index {index} ({width}x{height})")
            return cap
        cap.release()
    return None

cap = open_camera()
timestamp = 0

# Check if camera opened
if cap is None:
    print("Error: Could not open camera (tried indexes 0-2)")
    exit()

print("Press 'q' to quit")

# Main loop - runs continuously
while cap.isOpened():
    # Capture frame from camera
    valid, frame = cap.read()
    
    if not valid:
        print("Warning: Could not read frame")
        break
    
    # Convert BGR to RGB (MediaPipe needs RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Create MediaPipe image
    mp_image = mp.Image(
        image_format = mp.ImageFormat.SRGB,
        data = rgb_frame
    )
    
    # Detect hands in the frame
    result = landmarker.detect_for_video(mp_image, timestamp)
    timestamp += 1
    
    # If hands detected
    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            # Get finger landmark positions
            index_tip = hand[8]
            index_pip = hand[6]
            middle_tip = hand[12]
            middle_pip = hand[10]
            ring_tip = hand[16]
            ring_pip = hand[14]
            pinky_tip = hand[20]
            pinky_pip = hand[18]
            
            # Check if each finger is extended or folded
            index_extended = index_tip.y < index_pip.y
            middle_folded = middle_tip.y > middle_pip.y
            ring_folded = ring_tip.y > ring_pip.y
            pinky_folded = pinky_tip.y > pinky_pip.y
            
            # Check for pointing gesture and load appropriate meme
            if index_extended and middle_folded and ring_folded and pinky_folded:
                meme_image = cv2.imread(str(ASSETS / "meme" / "pointing.png"))
            else:
                meme_image = cv2.imread(str(ASSETS / "meme" / "staring.png"))

            # Draw green circles on all hand landmarks
            for lm in hand:
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
    else:
        # No hands detected - show default meme
        meme_image = cv2.imread(str(ASSETS / "meme" / "staring.png"))
    
    # Resize meme to match frame size
    frame_height, frame_width = frame.shape[:2]
    meme_resized = cv2.resize(meme_image, (frame_width, frame_height))
    
    # Combine meme and frame side-by-side
    combined = np.hstack([meme_resized, frame])
    
    # Display the result
    cv2.imshow('Think Monke', combined)
    
    # Exit if 'q' pressed
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
landmarker.close()
print("Application closed!")
