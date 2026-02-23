import cv2 
import mediapipe as mp 
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Load meme/staring.png



# Setup hand detection
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')

options = vision.HandLandmarkerOptions(
    base_options = base_options,
    num_hands = 2,
    running_mode = vision.RunningMode.VIDEO,
    min_hand_detection_confidence = 0.6,
    min_tracking_confidence = 0.6)

landmarker = vision.HandLandmarker.create_from_options(options)

# Open camera (try 0 if 1 doesn't work)


# Check if camera opened



print("Camera opened successfully!")

# Main loop

    


# Cleanup
cap.release()
cv2.destroyAllWindows()
landmarker.close()
print("Application closed!")
