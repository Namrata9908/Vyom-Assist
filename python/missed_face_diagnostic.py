import cv2
import os
import time


# ========================================
# Vyom Assist
# Step 3 - Missed Face Frame Diagnostic
# ========================================

MODEL_PATH = "face_detection_yunet_2026may.onnx"

CAMERA_INDEX = 0

TEST_DURATION = 30

FACE_THRESHOLD = 0.1

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

OUTPUT_FOLDER = "diagnostic_missed_frames"


# ========================================
# Create Output Folder
# ========================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ========================================
# Check Model
# ========================================

if not os.path.exists(MODEL_PATH):
    print()
    print("ERROR: YuNet model not found!")
    print()
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

saved_missed_frames = 0

start_time = time.time()


# ========================================
# Console Header
# ========================================

print()
print("========================================")
print("   Vyom Assist - Missed Face")
print("             Diagnostic")
print("========================================")
print()

print("Camera started.")
print("YuNet face detection started.")
print()

print(f"Camera size: {width} x {height}")
print(f"Test duration: {TEST_DURATION} seconds")
print(f"Face threshold: {FACE_THRESHOLD}")

print()
print("Missed frames will be saved here:")
print(OUTPUT_FOLDER)

print()
print("Look directly at the camera.")
print("Keep your face clearly visible.")

print()
print("Press Q to stop early.")
print()


# ========================================
# Main Loop
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


    # ========================================
    # Face Detected
    # ========================================

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


            # Face confidence
            confidence = float(face[14])


            cv2.putText(
                frame,
                f"Confidence: {confidence:.2f}",
                (x, max(20, y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )


    # ========================================
    # Face NOT Detected
    # ========================================

    else:

        face_not_detected_frames += 1


        # ------------------------------------
        # Save missed frame
        # ------------------------------------

        filename = os.path.join(
            OUTPUT_FOLDER,
            f"missed_{saved_missed_frames + 1:04d}_frame_{total_frames}.jpg"
        )


        cv2.imwrite(
            filename,
            frame
        )


        saved_missed_frames += 1


        # ------------------------------------
        # Display warning
        # ------------------------------------

        cv2.putText(
            frame,
            "FACE NOT DETECTED",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            3
        )


    # ========================================
    # Statistics
    # ========================================

    elapsed = time.time() - start_time


    detection_rate = 0

    if total_frames > 0:

        detection_rate = (
            face_detected_frames / total_frames
        ) * 100


    # ========================================
    # Display Counters
    # ========================================

    cv2.putText(
        frame,
        f"Total: {total_frames}",
        (10, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"Detected: {face_detected_frames}",
        (10, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2
    )


    cv2.putText(
        frame,
        f"Missed: {face_not_detected_frames}",
        (10, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 255),
        2
    )


    cv2.putText(
        frame,
        f"Rate: {detection_rate:.2f}%",
        (10, 165),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 0),
        2
    )


    # ========================================
    # Show Camera
    # ========================================

    cv2.imshow(
        "Vyom Assist - Missed Face Diagnostic",
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
# Final Statistics
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


# ========================================
# Final Output
# ========================================

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

print(f"Missed frames saved: {saved_missed_frames}")

print(f"Folder: {OUTPUT_FOLDER}")

print()

print("========================================")
print("             TEST COMPLETE")
print("========================================")
print()