import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Load meme/staring.png
meme_image = cv2.imread("meme/staring.png")
if meme_image is None:
    print("Error: Could not load meme image")
    exit()

# Setup hand detection
base_options = python.BaseOptions(model_asset_path='models/hand_landmarker.task')

options = vision.HandLandmarkerOptions(
    base_options = base_options,
    num_hands = 2,
    running_mode = vision.RunningMode.VIDEO,
    min_hand_detection_confidence = 0.6,
    min_tracking_confidence = 0.6)

landmarker = vision.HandLandmarker.create_from_options(options)

# Open camera (tries a few indexes in case index 0 isn't your webcam)
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

# Main loop
while cap.isOpened():
    pass  # TODO: remove this once you start filling in the sections below

    # Capture a frame and detect hands



    # Check for pointing gesture and draw landmarks



    # Combine meme and camera feed, then display



# Cleanup
cap.release()
cv2.destroyAllWindows()
landmarker.close()
print("Application closed!")
