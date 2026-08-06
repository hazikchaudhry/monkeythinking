import time
from collections import deque

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image, ImageSequence

WRIST, MIDDLE_MCP = 0, 9

# Tune these once you can see the live numbers on your camera
CLOSE_DISTANCE_PX = 300   # how close the two palm centers must be
RUB_WINDOW_SECONDS = 0.6   # how far back we look for back-and-forth motion
MIN_WIGGLE_PX = 0      # total movement needed within that window to count as rubbing
NET_VS_WIGGLE_RATIO = 0.6  # net drift must be well under total wiggle (i.e. it mostly cancels out)
MIN_SAMPLES = 5            # frames of history needed before judging motion
JAW_OPEN_THRESHOLD = 0.5   # jawOpen blendshape score (0-1) needed to count as "mouth wide open"
MIN_HOLD_SECONDS = 1.0     # keep whatever's on screen for at least this long before switching


def load_gif(path):
    """Decode every frame of a gif to BGR plus its display duration in seconds."""
    gif = Image.open(path)
    frames, durations = [], []
    for frame in ImageSequence.Iterator(gif):
        rgb = np.array(frame.convert("RGB"))
        frames.append(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
        durations.append(frame.info.get("duration", 100) / 1000.0)
    return frames, durations


def current_frame(frames, durations, total_duration, start_time):
    if total_duration <= 0:
        return frames[0]
    elapsed = (time.time() - start_time) % total_duration
    acc = 0.0
    for frame, duration in zip(frames, durations):
        acc += duration
        if elapsed < acc:
            return frame
    return frames[-1]


def landmark_px(hand, index, width, height):
    lm = hand[index]
    return np.array([lm.x * width, lm.y * height])


def palm_center(hand, width, height):
    return (landmark_px(hand, WRIST, width, height) + landmark_px(hand, MIDDLE_MCP, width, height)) / 2


def hands_rubbing(history):
    """True when the two palms have been wiggling back and forth rather than sitting still or sliding apart."""
    if len(history) < MIN_SAMPLES:
        return False, 0.0, 0.0

    points = [p for _, p in history]
    wiggle = sum(np.linalg.norm(points[i] - points[i - 1]) for i in range(1, len(points)))
    net_drift = np.linalg.norm(points[-1] - points[0])

    is_rubbing = wiggle > MIN_WIGGLE_PX and net_drift < wiggle * NET_VS_WIGGLE_RATIO
    return is_rubbing, wiggle, net_drift


def blendshape_score(blendshapes, name):
    return next((c.score for c in blendshapes if c.category_name == name), None)


# Initialize the hand landmark detection model
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')

options = vision.HandLandmarkerOptions(
    base_options = base_options,
    num_hands = 2,
    running_mode = vision.RunningMode.VIDEO,
    min_hand_detection_confidence = 0.6,
    min_tracking_confidence = 0.6)

landmarker = vision.HandLandmarker.create_from_options(options)

# Initialize the face landmark model (gives us blendshape scores like "jawOpen")
face_base_options = python.BaseOptions(model_asset_path='face_landmarker.task')

face_options = vision.FaceLandmarkerOptions(
    base_options = face_base_options,
    num_faces = 1,
    running_mode = vision.RunningMode.VIDEO,
    output_face_blendshapes = True)

face_landmarker = vision.FaceLandmarker.create_from_options(face_options)

# Decode every gif up front; the loop just picks a frame out of whichever list is active
wait_frames, wait_durations = load_gif("meme/wait.gif")
wait_total = sum(wait_durations)
cooking_frames, cooking_durations = load_gif("meme/cooking.gif")
cooking_total = sum(cooking_durations)
tongue_frames, tongue_durations = load_gif("meme/tounge.gif")
tongue_total = sum(tongue_durations)
start_time = time.time()

# Rolling history of (timestamp, relative palm position) used to detect rubbing motion
relative_position_history = deque()
last_print_time = 0.0
display_state = "waiting"
state_changed_at = time.time()

# Open the webcam (try 0 if 1 doesn't work on your machine)
cap = cv2.VideoCapture(1)
timestamp = 0

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

print("Camera opened successfully!")
print("Press 'q' to quit")

while cap.isOpened():
    valid, frame = cap.read()

    if not valid:
        print("Warning: Could not read frame")
        break

    frame_height, frame_width = frame.shape[:2]

    # MediaPipe expects RGB, OpenCV captures in BGR
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(
        image_format = mp.ImageFormat.SRGB,
        data = rgb_frame
    )

    result = landmarker.detect_for_video(mp_image, timestamp)
    timestamp += 1

    # Draw a dot on every detected landmark so you can see what the model is tracking
    hands_seen = len(result.hand_landmarks) if result.hand_landmarks else 0
    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            for lm in hand:
                cx, cy = int(lm.x * frame_width), int(lm.y * frame_height)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    cooking = False
    debug_lines = [f"hands seen: {hands_seen}"]

    if hands_seen == 2:
        hand_a, hand_b = result.hand_landmarks
        center_a = palm_center(hand_a, frame_width, frame_height)
        center_b = palm_center(hand_b, frame_width, frame_height)
        distance = np.linalg.norm(center_a - center_b)
        close = distance < CLOSE_DISTANCE_PX

        now = time.time()
        relative_position_history.append((now, center_a - center_b))
        while relative_position_history and now - relative_position_history[0][0] > RUB_WINDOW_SECONDS:
            relative_position_history.popleft()

        rubbing, wiggle, net_drift = hands_rubbing(relative_position_history)
        cooking = close and rubbing

        debug_lines.append(f"hand dist: {distance:.0f}px (need < {CLOSE_DISTANCE_PX})")
        debug_lines.append(f"wiggle: {wiggle:.0f}px (need > {MIN_WIGGLE_PX}) net: {net_drift:.0f}px")
    else:
        relative_position_history.clear()

    # The model has no tongue signal at all (confirmed by dumping every blendshape name it
    # produces), so "wide open mouth" (jawOpen) is used as the trigger for the tongue gif instead
    face_result = face_landmarker.detect_for_video(mp_image, timestamp)
    faces_seen = len(face_result.face_blendshapes) if face_result.face_blendshapes else 0
    debug_lines.append(f"face seen: {faces_seen}")

    jaw_open_score = 0.0
    if face_result.face_blendshapes:
        blendshapes = face_result.face_blendshapes[0]
        score = blendshape_score(blendshapes, "jawOpen")
        if score is not None:
            jaw_open_score = score

    mouth_open = jaw_open_score > JAW_OPEN_THRESHOLD
    # Mouth-open takes priority over the cooking gesture if somehow both happen at once
    raw_state = "TONGUE" if mouth_open else ("COOKING" if cooking else "waiting")

    # Only actually switch what's on screen once the current one has had its minimum lingertime
    current_time = time.time()
    if raw_state != display_state and current_time - state_changed_at >= MIN_HOLD_SECONDS:
        display_state = raw_state
        state_changed_at = current_time

    debug_lines.append(f"jaw open: {jaw_open_score:.2f} (need > {JAW_OPEN_THRESHOLD})")
    debug_lines.append(f"state: {display_state} (raw: {raw_state})")

    for i, line in enumerate(debug_lines):
        cv2.putText(frame, line, (10, 30 + i * 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    if current_time - last_print_time >= 0.3:
        print(" | ".join(debug_lines))
        last_print_time = current_time

    if display_state == "TONGUE":
        display_image = current_frame(tongue_frames, tongue_durations, tongue_total, start_time)
    elif display_state == "COOKING":
        display_image = current_frame(cooking_frames, cooking_durations, cooking_total, start_time)
    else:
        display_image = current_frame(wait_frames, wait_durations, wait_total, start_time)

    display_resized = cv2.resize(display_image, (frame_width, frame_height))
    combined = np.hstack([display_resized, frame])

    cv2.imshow('Think Monke', combined)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
landmarker.close()
face_landmarker.close()
print("Application closed!")
