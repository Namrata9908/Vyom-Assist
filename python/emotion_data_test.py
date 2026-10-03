import cv2
import os
import json
import numpy as np
from datetime import datetime


# ========================================
# Model Paths
# ========================================

FACE_MODEL = "face_detection_yunet_2026may.onnx"
EMOTION_MODEL = "facial_expression_recognition_mobilefacenet_2022july.onnx"


# ========================================
# Check Models
# ========================================

if not os.path.exists(FACE_MODEL):
    print("❌ Face detection model not found.")
    exit()

if not os.path.exists(EMOTION_MODEL):
    print("❌ Emotion model not found.")
    exit()


# ========================================
# Emotion Labels
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
# OpenCV Zoo standard 5 landmark points
# ========================================

REFERENCE_POINTS = np.array(
    [
        [38.2946, 51.6963],
        [73.5318, 51.5014],
        [56.0252, 71.7366],
        [41.5493, 92.3655],
        [70.7299, 92.2041]
    ],
    dtype=np.float32
)


def align_face(image, landmarks):

    landmarks = np.asarray(
        landmarks,
        dtype=np.float32
    )

    transform_matrix, _ = cv2.estimateAffinePartial2D(
        landmarks,
        REFERENCE_POINTS,
        method=cv2.LMEDS
    )

    if transform_matrix is None:
        return None

    aligned = cv2.warpAffine(
        image,
        transform_matrix,
        (112, 112),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0)
    )

    return aligned


# ========================================
# Emotion Preprocessing
# ========================================

def preprocess_emotion(face_image):

    face_image = cv2.cvtColor(
        face_image,
        cv2.COLOR_BGR2RGB
    )

    face_image = face_image.astype(
        np.float32
    )

    face_image = face_image / 255.0

    face_image = face_image - 0.5

    face_image = face_image / 0.5

    blob = cv2.dnn.blobFromImage(
        face_image
    )

    return blob


# ========================================
# Softmax
# ========================================

def softmax(values):

    values = np.asarray(
        values,
        dtype=np.float32
    )

    values = values - np.max(values)

    exp_values = np.exp(values)

    probabilities = (
        exp_values /
        np.sum(exp_values)
    )

    return probabilities


# ========================================
# Camera
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
# Face Detector
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
# Face Smoothing
# ========================================

smooth_x = None
smooth_y = None
smooth_w = None
smooth_h = None

SMOOTHING = 0.15


# ========================================
# Current Emotion
# ========================================

current_emotion = "Unknown"
current_confidence = 0.0


# ========================================
# Start
# ========================================

print("✅ Camera started.")
print("👤 Face detection started.")
print("😊 Emotion detection started.")
print("📊 Emotion data output started.")
print("🎯 Official OpenCV preprocessing enabled.")
print("📈 All 7 emotion scores will be displayed.")
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
    # Detect Face
    # ====================================

    _, faces = face_detector.detect(
        frame
    )


    # ====================================
    # Face Detected
    # ====================================

    if faces is not None and len(faces) > 0:

        # =================================
        # Select highest-confidence face
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
        # Smooth Coordinates
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
        # Face Coordinates
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
        # Validate Face
        # =================================

        if x2 <= x1 or y2 <= y1:
            continue


        # =================================
        # Get YuNet Landmarks
        # =================================

        landmarks = face[
            4:14
        ].reshape(
            5,
            2
        )


        # =================================
        # Align Face
        # =================================

        aligned_face = align_face(
            frame,
            landmarks
        )


        if aligned_face is None:
            continue


        # =================================
        # Emotion Preprocessing
        # =================================

        emotion_blob = preprocess_emotion(
            aligned_face
        )


        # =================================
        # Run Emotion Model
        # =================================

        emotion_model.setInput(
            emotion_blob,
            "data"
        )

        prediction = emotion_model.forward(
            ["label"]
        )


        # =================================
        # Handle OpenCV Tuple Output
        # =================================

        if isinstance(prediction, tuple):

            prediction = prediction[0]


        raw_scores = np.asarray(
            prediction,
            dtype=np.float32
        ).flatten()


        # =================================
        # Validate Output
        # =================================

        if len(raw_scores) != len(EMOTIONS):

            print(
                "⚠️ Unexpected emotion output size:",
                len(raw_scores)
            )

            continue


        # =================================
        # Convert Scores to Probabilities
        # =================================

        probabilities = softmax(
            raw_scores
        )


        # =================================
        # Print All Emotion Scores
        # =================================

        print("\n========== EMOTION SCORES ==========")

        for emotion_name, probability in zip(
            EMOTIONS,
            probabilities
        ):

            print(
                f"{emotion_name}: "
                f"{probability * 100:.2f}%"
            )

        print(
            "====================================\n",
            flush=True
        )


        # =================================
        # Highest Probability
        # =================================

        emotion_index = int(
            np.argmax(probabilities)
        )


        # =================================
        # Emotion
        # =================================

        current_emotion = EMOTIONS[
            emotion_index
        ]


        # =================================
        # Confidence
        # =================================

        current_confidence = float(
            probabilities[
                emotion_index
            ]
        )


        confidence_percent = (
            current_confidence * 100
        )


        # =================================
        # Emotion Data
        # =================================

        emotion_data = {

            "emotion": current_emotion,

            "confidence": round(
                current_confidence,
                4
            ),

            "confidence_percent": round(
                confidence_percent,
                2
            ),

            "face_detected": True,

            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            )
        }


        # =================================
        # Print JSON
        # =================================

        print(
            json.dumps(
                emotion_data
            ),
            flush=True
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
                2,
                (255, 0, 0),
                -1
            )


        # =================================
        # Display Emotion
        # =================================

        label = (
            f"{current_emotion} "
            f"({confidence_percent:.1f}%)"
        )


        cv2.putText(
            frame,
            label,
            (
                x1,
                max(y1 - 10, 20)
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


    # ====================================
    # No Face
    # ====================================

    else:

        current_emotion = "Unknown"
        current_confidence = 0.0


        emotion_data = {

            "emotion": "Unknown",

            "confidence": 0.0,

            "confidence_percent": 0.0,

            "face_detected": False,

            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            )
        }


        print(
            json.dumps(
                emotion_data
            ),
            flush=True
        )


    # ====================================
    # Show Camera
    # ====================================

    cv2.imshow(
        "Vyom Assist - Emotion Data Test",
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


print(
    "✅ Emotion data test closed."
)
