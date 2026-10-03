import cv2
import os
import time


# ========================================
# Vyom Assist
# Emotion Pipeline Diagnostic - Step 2
# ========================================

MODEL_PATH = "face_detection_yunet_2026may.onnx"

CAMERA_INDEX = 0
TEST_DURATION = 30

FACE_THRESHOLD = 0.1

FRAME_WIDTH = 640
FRAME_HEIGHT = 480


# ========================================
# Check Model
# ========================================

if not os.path.exists(MODEL_PATH):
    print()
    print("ERROR: YuNet model not found!")
    print("Expected:")
    print(MODEL_PATH)
    print()
    input("Press Enter to exit...")
    raise SystemExit


# ========================================
# Start Camera
# ========================================

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print()
    print("ERROR: Could not open camera.")
    print()
    input("Press Enter to exit...")
    raise SystemExit


cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)


# ========================================
# Read First Frame
# ========================================

ret, frame = cap.read()

if not ret:
    print()
    print("ERROR: Could not read first camera frame.")
    cap.release()
    input("Press Enter to exit...")
    raise SystemExit


height, width = frame.shape[:2]


# ========================================
# Create YuNet Detector
# ========================================

detector = cv2.FaceDetectorYN.create(
    MODEL_PATH,
    "",
    (width, height),
    FACE_THRESHOLD,
    0.3,
    5000
)


# ========================================
# Counters
# ========================================

total_frames = 0
face_detected_frames = 0
face_not_detected_frames = 0

start_time = time.time()


print()
print("========================================")
print("   Vyom Assist - Emotion Pipeline")
print("          Diagnostic - Step 2")
print("========================================")
print()
print("Camera started.")
print("YuNet face detection started.")
print()
print(f"Camera size: {width} x {height}")
print(f"Test duration: {TEST_DURATION} seconds")
print(f"Face threshold: {FACE_THRESHOLD}")
print()
print("Look directly at the camera.")
print("Keep your face clearly visible.")
print()
print("Press Q to stop early.")
print()


# ========================================
# Main Test Loop
# ========================================

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    total_frames += 1

    # ----------------------------------------
    # Face Detection
    # ----------------------------------------

    _, faces = detector.detect(frame)

    face_found = (
        faces is not None
        and len(faces) > 0
    )

    if face_found:

        face_detected_frames += 1

        for face in faces:

            x, y, w, h = face[:4].astype(int)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

    else:

        face_not_detected_frames += 1


    # ========================================
    # Current Statistics
    # ========================================

    elapsed = time.time() - start_time

    detection_rate = 0

    if total_frames > 0:
        detection_rate = (
            face_detected_frames / total_frames
        ) * 100

    current_fps = 0

    if elapsed > 0:
        current_fps = total_frames / elapsed


    # ========================================
    # Display
    # ========================================

    cv2.putText(
        frame,
        f"Frames: {total_frames}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Face Detected: {face_detected_frames}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Face NOT Detected: {face_not_detected_frames}",
        (10, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        f"Detection Rate: {detection_rate:.2f}%",
        (10, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"FPS: {current_fps:.2f}",
        (10, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    cv2.imshow(
        "Vyom Assist - Emotion Pipeline Diagnostic",
        frame
    )


    # ========================================
    # Stop Conditions
    # ========================================

    if elapsed >= TEST_DURATION:
        break

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ========================================
# Cleanup
# ========================================

cap.release()
cv2.destroyAllWindows()


# ========================================
# Final Results
# ========================================

elapsed = time.time() - start_time

if total_frames > 0:

    detection_rate = (
        face_detected_frames / total_frames
    ) * 100

    miss_rate = (
        face_not_detected_frames / total_frames
    ) * 100

else:

    detection_rate = 0
    miss_rate = 0


average_fps = 0

if elapsed > 0:
    average_fps = total_frames / elapsed


print()
print()
print("========================================")
print("          FINAL DIAGNOSTIC")
print("========================================")
print()
print(f"Test time: {elapsed:.2f} seconds")
print(f"Camera size: {width} x {height}")
print(f"Total frames: {total_frames}")
print(f"Face detected: {face_detected_frames}")
print(f"Face NOT detected: {face_not_detected_frames}")
print(f"Detection rate: {detection_rate:.2f}%")
print(f"Miss rate: {miss_rate:.2f}%")
print(f"Average FPS: {average_fps:.2f}")
print()
print("========================================")
print("             TEST COMPLETE")
print("========================================")
print()