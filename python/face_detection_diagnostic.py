import cv2
import os
import time


# ========================================
# Model Path
# ========================================

FACE_MODEL = "face_detection_yunet_2026may.onnx"


# ========================================
# Test Settings
# ========================================

WIDTH = 640
HEIGHT = 480

FACE_SCORE_THRESHOLD = 0.1

TEST_DURATION_SECONDS = 30


# ========================================
# Check Model
# ========================================

if not os.path.exists(FACE_MODEL):

    print("❌ Face detection model not found.")

    print(
        f"Expected file: {FACE_MODEL}"
    )

    exit()


# ========================================
# Camera
# ========================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("❌ Camera could not be opened.")

    exit()


camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    WIDTH
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    HEIGHT
)


# ========================================
# YuNet Face Detector
# ========================================

face_detector = cv2.FaceDetectorYN_create(
    FACE_MODEL,
    "",
    (WIDTH, HEIGHT),
    FACE_SCORE_THRESHOLD,
    0.3,
    5000
)


# ========================================
# Counters
# ========================================

total_frames = 0

face_detected_frames = 0

face_not_detected_frames = 0


# ========================================
# Start Test
# ========================================

start_time = time.time()

print()
print("========================================")
print("   Vyom Assist - Face Detection")
print("             Diagnostic")
print("========================================")
print()

print("📷 Camera started.")
print("👤 YuNet face detection started.")
print()
print(
    f"⏱️ Test duration: {TEST_DURATION_SECONDS} seconds"
)
print(
    "🎯 Face threshold:",
    FACE_SCORE_THRESHOLD
)
print()
print("Look directly at the camera.")
print("Try to keep your face visible.")
print()
print("Press Q to stop early.")
print()


# ========================================
# Main Loop
# ========================================

while True:

    # ------------------------------------
    # Check Test Duration
    # ------------------------------------

    elapsed_time = (
        time.time() - start_time
    )

    if elapsed_time >= TEST_DURATION_SECONDS:

        break


    # ------------------------------------
    # Read Frame
    # ------------------------------------

    success, frame = camera.read()

    if not success:

        print(
            "❌ Failed to read camera frame."
        )

        break


    total_frames += 1


    # ------------------------------------
    # Set Input Size
    # ------------------------------------

    face_detector.setInputSize(
        (
            frame.shape[1],
            frame.shape[0]
        )
    )


    # ------------------------------------
    # Detect Face
    # ------------------------------------

    _, faces = face_detector.detect(
        frame
    )


    # ====================================
    # Face Detected
    # ====================================

    if faces is not None and len(faces) > 0:

        face_detected_frames += 1

        status_text = "FACE DETECTED"

        status_color = (
            0,
            255,
            0
        )


        # -------------------------------
        # Select Best Face
        # -------------------------------

        face = max(
            faces,
            key=lambda item: item[14]
        )


        # -------------------------------
        # Face Coordinates
        # -------------------------------

        x = int(face[0])
        y = int(face[1])
        w = int(face[2])
        h = int(face[3])


        # -------------------------------
        # Face Confidence
        # -------------------------------

        face_confidence = float(
            face[14]
        )


        # -------------------------------
        # Draw Rectangle
        # -------------------------------

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            status_color,
            2
        )


        # -------------------------------
        # Display Confidence
        # -------------------------------

        cv2.putText(
            frame,
            f"Face score: {face_confidence:.3f}",
            (
                10,
                30
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            status_color,
            2
        )


    # ====================================
    # Face NOT Detected
    # ====================================

    else:

        face_not_detected_frames += 1

        status_text = "FACE NOT DETECTED"

        status_color = (
            0,
            0,
            255
        )


    # ====================================
    # Calculate Live Percentage
    # ====================================

    if total_frames > 0:

        detection_percentage = (
            face_detected_frames
            / total_frames
        ) * 100

        missed_percentage = (
            face_not_detected_frames
            / total_frames
        ) * 100

    else:

        detection_percentage = 0.0

        missed_percentage = 0.0


    # ====================================
    # Display Status
    # ====================================

    cv2.putText(
        frame,
        status_text,
        (
            10,
            60
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        status_color,
        2
    )


    # ====================================
    # Display Statistics
    # ====================================

    cv2.putText(
        frame,
        f"Frames: {total_frames}",
        (
            10,
            95
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"Detected: {face_detected_frames}",
        (
            10,
            125
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"Not detected: {face_not_detected_frames}",
        (
            10,
            155
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"Detection: {detection_percentage:.1f}%",
        (
            10,
            185
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # ====================================
    # Display Timer
    # ====================================

    remaining = max(
        0,
        TEST_DURATION_SECONDS - elapsed_time
    )

    cv2.putText(
        frame,
        f"Time left: {remaining:.1f}s",
        (
            10,
            220
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # ====================================
    # Show Camera
    # ====================================

    cv2.imshow(
        "Vyom Assist - Face Detection Diagnostic",
        frame
    )


    # ====================================
    # Quit With Q
    # ====================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ========================================
# Cleanup
# ========================================

camera.release()

cv2.destroyAllWindows()


# ========================================
# Final Statistics
# ========================================

total_time = (
    time.time() - start_time
)


if total_frames > 0:

    final_detection_percentage = (
        face_detected_frames
        / total_frames
    ) * 100

    final_missed_percentage = (
        face_not_detected_frames
        / total_frames
    ) * 100

else:

    final_detection_percentage = 0.0

    final_missed_percentage = 0.0


# ========================================
# Final Report
# ========================================

print()
print("========================================")
print("          FINAL DIAGNOSTIC")
print("========================================")
print()

print(
    f"⏱️ Test time: {total_time:.2f} seconds"
)

print(
    f"🎞️ Total frames: {total_frames}"
)

print(
    f"✅ Face detected: {face_detected_frames}"
)

print(
    f"❌ Face NOT detected: {face_not_detected_frames}"
)

print(
    f"📊 Detection rate: "
    f"{final_detection_percentage:.2f}%"
)

print(
    f"📉 Miss rate: "
    f"{final_missed_percentage:.2f}%"
)

print()

print("========================================")
print("             TEST COMPLETE")
print("========================================")