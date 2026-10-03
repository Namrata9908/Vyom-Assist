import cv2
import os

MODEL_PATH = "face_detection_yunet_2026may.onnx"

if not os.path.exists(MODEL_PATH):
    print("❌ YuNet model file not found.")
    exit()

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened.")
    exit()

# Initial camera size
width = 640
height = 480

camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# OpenCV 5 + YuNet face detector
detector = cv2.FaceDetectorYN_create(
    MODEL_PATH,
    "",
    (width, height),
    0.1,
    0.3,
    5000
)

print("✅ Camera started.")
print("👤 YuNet face detection started.")
print("Press Q to close.")

while True:

    success, frame = camera.read()

    if not success:
        print("❌ Failed to read camera frame.")
        break

    # Update detector input size
    detector.setInputSize(
        (frame.shape[1], frame.shape[0])
    )

    # Detect faces
    _, faces = detector.detect(frame)

    if faces is not None:

        for face in faces:

            x = int(face[0])
            y = int(face[1])
            w = int(face[2])
            h = int(face[3])

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Face Detected",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    cv2.imshow(
        "Vyom Assist - Face Detection Test",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

print("✅ Camera test closed.")