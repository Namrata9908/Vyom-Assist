import cv2
import os
import numpy as np


# ========================================
# Model Paths
# ========================================

FACE_MODEL = "face_detection_yunet_2026may.onnx"
EMOTION_MODEL = "facial_expression_recognition_mobilefacenet_2022july.onnx"


# ========================================
# Check Model Files
# ========================================

if not os.path.exists(FACE_MODEL):
    print("❌ Face detection model not found.")
    exit()

if not os.path.exists(EMOTION_MODEL):
    print("❌ Emotion model not found.")
    exit()


# ========================================
# Face Alignment
# OpenCV Zoo official preprocessing
# ========================================

class FaceAlignment:

    def __init__(self):

        # Standard 5 facial landmark positions
        # for 112 x 112 input.
        self.std_points = np.array(
            [
                [38.2946, 51.6963],
                [73.5318, 51.5014],
                [56.0252, 71.7366],
                [41.5493, 92.3655],
                [70.7299, 92.2041]
            ],
            dtype=np.float32
        )


    def find_similarity_transform(self, src_pts, dst_pts):

        src_pts = np.asarray(src_pts, dtype=np.float32)
        dst_pts = np.asarray(dst_pts, dtype=np.float32)

        # Center points
        src_mean = np.mean(src_pts, axis=0)
        dst_mean = np.mean(dst_pts, axis=0)

        src_centered = src_pts - src_mean
        dst_centered = dst_pts - dst_mean

        # Scale
        src_norm = np.sqrt(
            np.sum(src_centered ** 2)
        )

        dst_norm = np.sqrt(
            np.sum(dst_centered ** 2)
        )

        if src_norm < 1e-6:
            raise ValueError("Invalid source landmarks.")

        if dst_norm < 1e-6:
            raise ValueError("Invalid destination landmarks.")

        src_scaled = src_centered / src_norm
        dst_scaled = dst_centered / dst_norm

        # SVD
        H = src_scaled.T @ dst_scaled

        U, _, Vt = np.linalg.svd(H)

        R = Vt.T @ U.T

        # Prevent reflection
        if np.linalg.det(R) < 0:
            Vt[-1, :] *= -1
            R = Vt.T @ U.T

        scale = dst_norm / src_norm

        A = scale * R

        translation = dst_mean - A @ src_mean

        transform = np.zeros((2, 3), dtype=np.float32)

        transform[:, :2] = A
        transform[:, 2] = translation

        return transform


    def get_align_image(self, image, landmarks):

        landmarks = np.asarray(
            landmarks,
            dtype=np.float32
        ).reshape(5, 2)

        transform = self.find_similarity_transform(
            landmarks,
            self.std_points
        )

        aligned = cv2.warpAffine(
            image,
            transform,
            (112, 112)
        )

        return aligned


# ========================================
# Start Camera
# ========================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("❌ Camera could not be opened.")
    exit()


width = 640
height = 480

camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    width
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    height
)


# ========================================
# YuNet Face Detector
# ========================================

face_detector = cv2.FaceDetectorYN_create(
    FACE_MODEL,
    "",
    (width, height),
    0.1,
    0.3,
    5000
)


# ========================================
# Emotion Model
# ========================================

emotion_model = cv2.dnn.readNetFromONNX(
    EMOTION_MODEL
)


# ========================================
# Emotion Labels
# Official OpenCV Zoo order
# ========================================

EMOTIONS = [
    "Angry",
    "Disgust",
    "Fearful",
    "Happy",
    "Neutral",
    "Sad",
    "Surprised"
]


# ========================================
# Face Alignment
# ========================================

face_alignment = FaceAlignment()


# ========================================
# Face Box Smoothing
# ========================================

smooth_x = None
smooth_y = None
smooth_w = None
smooth_h = None

SMOOTHING = 0.15


# ========================================
# Start
# ========================================

print("✅ Camera started.")
print("👤 Face detection started.")
print("😊 Emotion detection started.")
print("🎯 Official OpenCV face alignment enabled.")
print("📐 112x112 + RGB + official normalization enabled.")
print("Press Q to close.")


# ========================================
# Main Loop
# ========================================

while True:

    success, frame = camera.read()

    if not success:

        print("❌ Failed to read camera frame.")
        break


    # ====================================
    # Detect Faces
    # ====================================

    # Keep detector input size synchronized
    # with the actual camera frame.
    face_detector.setInputSize(
        (frame.shape[1], frame.shape[0])
    )

    _, faces = face_detector.detect(frame)


    if faces is not None and len(faces) > 0:

        # =================================
        # Highest-confidence face
        # =================================

        face = max(
            faces,
            key=lambda item: item[14]
        )


        # =================================
        # Raw Face Coordinates
        # =================================

        raw_x = float(face[0])
        raw_y = float(face[1])
        raw_w = float(face[2])
        raw_h = float(face[3])


        # =================================
        # Smooth Face Coordinates
        # =================================

        if smooth_x is None:

            smooth_x = raw_x
            smooth_y = raw_y
            smooth_w = raw_w
            smooth_h = raw_h

        else:

            smooth_x = (
                SMOOTHING * raw_x
                + (1 - SMOOTHING) * smooth_x
            )

            smooth_y = (
                SMOOTHING * raw_y
                + (1 - SMOOTHING) * smooth_y
            )

            smooth_w = (
                SMOOTHING * raw_w
                + (1 - SMOOTHING) * smooth_w
            )

            smooth_h = (
                SMOOTHING * raw_h
                + (1 - SMOOTHING) * smooth_h
            )


        # =================================
        # Integer Coordinates
        # =================================

        x1 = max(
            0,
            int(smooth_x)
        )

        y1 = max(
            0,
            int(smooth_y)
        )

        x2 = min(
            frame.shape[1],
            int(smooth_x + smooth_w)
        )

        y2 = min(
            frame.shape[0],
            int(smooth_y + smooth_h)
        )


        # =================================
        # Official Emotion Preprocessing
        # =================================

        # IMPORTANT:
        # Do NOT crop using x1:y1:x2:y2
        # for emotion recognition.
        #
        # The official OpenCV model uses
        # YuNet's 5 landmarks to align
        # the complete face.


        # YuNet format:
        #
        # face[0:4]   = x, y, width, height
        # face[4:14]  = 5 landmarks
        # face[14]    = confidence
        #
        # Landmarks:
        # right eye
        # left eye
        # nose
        # right mouth corner
        # left mouth corner

        landmarks = face[4:14].reshape(
            5,
            2
        )


        try:

            # =================================
            # Face Alignment
            # =================================

            aligned_face = face_alignment.get_align_image(
                frame,
                landmarks
            )


            # =================================
            # BGR -> RGB
            # =================================

            aligned_face = cv2.cvtColor(
                aligned_face,
                cv2.COLOR_BGR2RGB
            )


            # =================================
            # Convert to float32
            # =================================

            aligned_face = aligned_face.astype(
                np.float32
            )


            # =================================
            # Normalize
            #
            # Official OpenCV Zoo:
            #
            # image / 255
            # image - 0.5
            # image / 0.5
            #
            # Result range approximately:
            # [-1, +1]
            # =================================

            aligned_face = (
                aligned_face / 255.0
            )

            aligned_face = (
                aligned_face - 0.5
            )

            aligned_face = (
                aligned_face / 0.5
            )


            # =================================
            # Create DNN Blob
            # =================================

            emotion_blob = cv2.dnn.blobFromImage(
                aligned_face
            )


            # =================================
            # Emotion Inference
            # =================================

            emotion_model.setInput(
                emotion_blob,
                "data"
            )


            prediction = emotion_model.forward(
                ["label"]
            )


            # =================================
            # Prediction Processing
            # =================================

            output = prediction[0]


            # Flatten if necessary
            output = np.asarray(
                output
            ).flatten()


            emotion_index = int(
                np.argmax(output)
            )


            # Safety check
            if (
                emotion_index < 0
                or emotion_index >= len(EMOTIONS)
            ):
                emotion = "Unknown"
                confidence = 0.0

            else:

                emotion = EMOTIONS[
                    emotion_index
                ]

                confidence = float(
                    output[emotion_index]
                )


            confidence_percent = (
                confidence * 100
            )


            # =================================
            # Draw Face Rectangle
            # =================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # =================================
            # Draw Landmarks
            # =================================

            for point in landmarks:

                px = int(point[0])
                py = int(point[1])

                cv2.circle(
                    frame,
                    (px, py),
                    3,
                    (255, 0, 255),
                    -1
                )


            # =================================
            # Emotion Label
            # =================================

            label = (
                f"{emotion} "
                f"({confidence_percent:.1f}%)"
            )


            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )


        except Exception as error:

            print(
                "Emotion processing error:",
                error
            )


    # ====================================
    # Show Camera
    # ====================================

    cv2.imshow(
        "Vyom Assist - Emotion Detection",
        frame
    )


    # ====================================
    # Quit
    # ====================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ========================================
# Cleanup
# ========================================

camera.release()

cv2.destroyAllWindows()

print("✅ Emotion test closed.")
