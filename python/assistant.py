from flask import Flask, jsonify, request
from datetime import datetime
import platform
import psutil
import socket
import cv2
import os
import numpy as np


app = Flask(__name__)


# ========================================
# CORS Configuration
# ========================================

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# ============================================================
# MODEL PATHS
# ============================================================

FACE_MODEL = "face_detection_yunet_2026may.onnx"
EMOTION_MODEL = "facial_expression_recognition_mobilefacenet_2022july.onnx"


# ============================================================
# CHECK MODELS
# ============================================================

if not os.path.exists(FACE_MODEL):
    print(f"❌ Face detection model not found: {FACE_MODEL}")

if not os.path.exists(EMOTION_MODEL):
    print(f"❌ Emotion model not found: {EMOTION_MODEL}")


# ============================================================
# EMOTION LABELS
# ============================================================

EMOTIONS = [
    "Angry",
    "Disgust",
    "Fearful",
    "Happy",
    "Neutral",
    "Sad",
    "Surprised"
]


# ============================================================
# FACE ALIGNMENT
# OpenCV Zoo standard 5 landmark reference points
# ============================================================

REFERENCE_POINTS = np.array(
    [
        [38.2946, 51.6963],   # Left eye
        [73.5318, 51.5014],   # Right eye
        [56.0252, 71.7366],   # Nose
        [41.5493, 92.3655],   # Left mouth
        [70.7299, 92.2041]    # Right mouth
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


# ============================================================
# EMOTION PREPROCESSING
# ============================================================

def preprocess_emotion(face_image):

    # BGR -> RGB
    face_image = cv2.cvtColor(
        face_image,
        cv2.COLOR_BGR2RGB
    )

    # Convert to float32
    face_image = face_image.astype(
        np.float32
    )

    # 0-255 -> 0-1
    face_image = face_image / 255.0

    # Mean = 0.5
    face_image = face_image - 0.5

    # Std = 0.5
    face_image = face_image / 0.5

    # Create DNN blob
    blob = cv2.dnn.blobFromImage(
        face_image
    )

    return blob


# ============================================================
# SOFTMAX
# ============================================================

def softmax(values):

    values = np.asarray(
        values,
        dtype=np.float32
    )

    values = values - np.max(values)

    exp_values = np.exp(values)

    probabilities = (
        exp_values
        / np.sum(exp_values)
    )

    return probabilities


# ============================================================
# EMOTION MODEL LOADING
# ============================================================

emotion_model = None

if os.path.exists(EMOTION_MODEL):

    try:

        emotion_model = cv2.dnn.readNetFromONNX(
            EMOTION_MODEL
        )

        print("✅ Emotion model loaded.")

    except Exception as error:

        print(
            f"❌ Could not load emotion model: {error}"
        )


# ============================================================
# FACE DETECTOR CREATION
# ============================================================

face_detector = None


# ============================================================
# GET EMOTION FROM CAMERA
# ============================================================

def detect_emotion_from_camera():

    global face_detector

    if emotion_model is None:

        return {
            "success": False,
            "emotion": "Unknown",
            "confidence": 0.0,
            "confidence_percent": 0.0,
            "face_detected": False,
            "message": "Emotion model is not available."
        }


    # --------------------------------------------------------
    # Open camera
    # --------------------------------------------------------

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        return {
            "success": False,
            "emotion": "Unknown",
            "confidence": 0.0,
            "confidence_percent": 0.0,
            "face_detected": False,
            "message": "Camera could not be opened."
        }


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


    # --------------------------------------------------------
    # Create detector
    # --------------------------------------------------------

    face_detector = cv2.FaceDetectorYN_create(
        FACE_MODEL,
        "",
        (width, height),
        0.1,
        0.3,
        5000
    )


    # --------------------------------------------------------
    # Read a few frames
    # --------------------------------------------------------

    detected_result = None


    for _ in range(5):

        success, frame = camera.read()

        if not success:
            continue


        # ----------------------------------------------------
        # Face detection
        # ----------------------------------------------------

        _, faces = face_detector.detect(
            frame
        )


        if faces is None or len(faces) == 0:

            continue


        # ----------------------------------------------------
        # Select highest-confidence face
        # ----------------------------------------------------

        face = max(
            faces,
            key=lambda item: item[14]
        )


        # ----------------------------------------------------
        # Get 5 landmarks
        # ----------------------------------------------------

        landmarks = face[
            4:14
        ].reshape(
            5,
            2
        )


        # ----------------------------------------------------
        # Align face
        # ----------------------------------------------------

        aligned_face = align_face(
            frame,
            landmarks
        )


        if aligned_face is None:

            continue


        # ----------------------------------------------------
        # Preprocess
        # ----------------------------------------------------

        emotion_blob = preprocess_emotion(
            aligned_face
        )


        # ----------------------------------------------------
        # Run model
        # ----------------------------------------------------

        emotion_model.setInput(
            emotion_blob,
            "data"
        )


        prediction = emotion_model.forward(
            ["label"]
        )


        # ----------------------------------------------------
        # OpenCV may return tuple
        # ----------------------------------------------------

        if isinstance(
            prediction,
            tuple
        ):

            prediction = prediction[0]


        # ----------------------------------------------------
        # Convert output to array
        # ----------------------------------------------------

        raw_scores = np.asarray(
            prediction
        ).flatten()


        # ----------------------------------------------------
        # Convert to probabilities
        # ----------------------------------------------------

        probabilities = softmax(
            raw_scores
        )


        # ----------------------------------------------------
        # Highest probability
        # ----------------------------------------------------

        emotion_index = int(
            np.argmax(probabilities)
        )


        current_emotion = EMOTIONS[
            emotion_index
        ]


        current_confidence = float(
            probabilities[
                emotion_index
            ]
        )


        confidence_percent = (
            current_confidence * 100
        )


        detected_result = {

            "success": True,

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
            ),

            "message": (
                f"Detected emotion: "
                f"{current_emotion}"
            )
        }


        # We have a valid result
        break


    # --------------------------------------------------------
    # Release camera
    # --------------------------------------------------------

    camera.release()


    # --------------------------------------------------------
    # No valid face/emotion
    # --------------------------------------------------------

    if detected_result is None:

        return {

            "success": False,

            "emotion": "Unknown",

            "confidence": 0.0,

            "confidence_percent": 0.0,

            "face_detected": False,

            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),

            "message": (
                "No face was detected."
            )
        }


    return detected_result


# ============================================================
# COMMON COMMAND NORMALIZER
# ============================================================

def normalize_command(command):

    command = command.strip().lower()

    command = " ".join(
        command.split()
    )

    command = command.rstrip(
        ".!?"
    )


    # ========================================================
    # GREETING ALIASES
    # ========================================================

    greeting_aliases = {

        "hello vyom assist": "hello",
        "hello vyom": "hello",

        "hi vyom assist": "hi",
        "hi vyom": "hi",

        "hey vyom assist": "hey",
        "hey vyom": "hey"
    }


    if command in greeting_aliases:

        command = greeting_aliases[
            command
        ]


    # ========================================================
    # REMOVE POLITE PREFIXES
    # ========================================================

    prefixes_to_remove = [

        "please ",
        "can you ",
        "could you ",
        "would you ",
        "will you ",
        "kindly ",
        "vyom assist ",
        "vyom "
    ]


    changed = True


    while changed:

        changed = False


        for prefix in prefixes_to_remove:

            if command.startswith(prefix):

                command = command[
                    len(prefix):
                ].strip()

                changed = True

                break


    # ========================================================
    # OPEN PREFIXES
    # ========================================================

    open_prefixes = [

        "launch ",
        "start ",
        "go to ",
        "visit "
    ]


    for prefix in open_prefixes:

        if command.startswith(prefix):

            command = (
                "open "
                + command[
                    len(prefix):
                ].strip()
            )

            break


    # ========================================================
    # PC / LAPTOP NORMALIZATION
    # ========================================================

    command = command.replace(
        "my pc",
        "my computer"
    )

    command = command.replace(
        "the pc",
        "the computer"
    )


    if command == "pc":

        command = "computer"


    command = command.replace(
        "my laptop",
        "my computer"
    )

    command = command.replace(
        "the laptop",
        "the computer"
    )


    if command == "laptop":

        command = "computer"


    # ========================================================
    # REBOOT -> RESTART
    # ========================================================

    if command.startswith(
        "reboot "
    ):

        command = (
            "restart "
            + command[7:].strip()
        )

    elif command == "reboot":

        command = "restart"


    # ========================================================
    # TIME
    # ========================================================

    if command in [

        "what is the time",
        "what's the time",
        "whats the time",
        "tell me the time",
        "tell me what's the time",
        "tell me whats the time"

    ]:

        command = "what time is it"


    # ========================================================
    # DATE
    # ========================================================

    if command in [

        "what is the date",
        "what's today's date",
        "what’s today's date",
        "what's today’s date",
        "what’s today’s date",
        "whats today's date",
        "tell me today's date",
        "tell me today’s date",
        "tell me todays date"

    ]:

        command = "what is today's date"


    # ========================================================
    # LOCK
    # ========================================================

    if command in [

        "lock my computer",
        "lock the computer",
        "lock my pc",
        "lock the pc",
        "lock my laptop",
        "lock the laptop"

    ]:

        command = "lock computer"


    # ========================================================
    # SHUTDOWN
    # ========================================================

    if command in [

        "shutdown my computer",
        "shutdown the computer",
        "shut down my computer",
        "shut down the computer",
        "shutdown my pc",
        "shutdown the pc",
        "shut down my pc",
        "shut down the pc",
        "shutdown my laptop",
        "shutdown the laptop",
        "shut down my laptop",
        "shut down the laptop"

    ]:

        command = "shutdown computer"


    # ========================================================
    # RESTART
    # ========================================================

    if command in [

        "restart my computer",
        "restart the computer",
        "restart my pc",
        "restart the pc",
        "restart my laptop",
        "restart the laptop"

    ]:

        command = "restart computer"


    # ========================================================
    # SEARCH
    # ========================================================

    search_prefixes = [

        "google ",
        "search for ",
        "look up ",
        "find "

    ]


    for prefix in search_prefixes:

        if command.startswith(prefix):

            command = (
                "search "
                + command[
                    len(prefix):
                ].strip()
            )

            break


    return command


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return (
        "Vyom Assist Python Assistant is running!"
    )


# ============================================================
# HEALTH
# ============================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "OK",

        "message":
            "Python assistant is healthy"

    })


# ============================================================
# EMOTION API
# ============================================================

@app.route(
    "/emotion",
    methods=["GET"]
)
def emotion():

    result = detect_emotion_from_camera()

    return jsonify(
        result
    )


# ============================================================
# ASSISTANT
# ============================================================

@app.route(
    "/assistant",
    methods=["POST"]
)
def assistant():

    data = request.get_json() or {}


    command = normalize_command(
        data.get(
            "command",
            ""
        )
    )


    # ========================================================
    # GREETINGS
    # ========================================================

    if command in [

        "hello",
        "hi",
        "hey",
        "vyom",
        "good morning",
        "good afternoon",
        "good evening",
        "good night"

    ]:

        if command == "good morning":

            message = (
                "Good morning! "
                "How can I help you?"
            )

        elif command == "good afternoon":

            message = (
                "Good afternoon! "
                "How can I help you?"
            )

        elif command == "good evening":

            message = (
                "Good evening! "
                "How can I help you?"
            )

        elif command == "good night":

            message = (
                "Good night! "
                "Have a great day ahead!"
            )

        else:

            message = (
                "Hello! I am Vyom Assist. "
                "How can I help you?"
            )


        return jsonify({

            "receivedCommand": command,

            "action": "greeting",

            "message": message

        })


    # ========================================================
    # HOW ARE YOU
    # ========================================================

    if command == "how are you":

        return jsonify({

            "receivedCommand": command,

            "action": "greeting",

            "message":
                "I am doing great! "
                "How can I help you?"

        })


    # ========================================================
    # NAME
    # ========================================================

    if command == "what is your name":

        return jsonify({

            "receivedCommand": command,

            "action": "greeting",

            "message":
                "My name is Vyom Assist."

        })


    # ========================================================
    # TIME
    # ========================================================

    if command == "what time is it":

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )


        return jsonify({

            "receivedCommand": command,

            "action": "time",

            "message":
                f"The current time is "
                f"{current_time}."

        })


    # ========================================================
    # DATE
    # ========================================================

    if command == "what is today's date":

        current_date = datetime.now().strftime(
            "%d %B %Y"
        )


        return jsonify({

            "receivedCommand": command,

            "action": "date",

            "message":
                f"Today's date is "
                f"{current_date}."

        })


    # ========================================================
    # SYSTEM INFORMATION
    # ========================================================

    if command in [

        "system information",
        "system info",
        "computer information",
        "computer info",
        "what computer am i using",
        "what operating system am i using"

    ]:

        system_name = platform.system()

        system_release = platform.release()

        machine = platform.machine()


        return jsonify({

            "receivedCommand": command,

            "action": "system_info",

            "system": system_name,

            "release": system_release,

            "machine": machine,

            "message": (
                f"You are using "
                f"{system_name} "
                f"{system_release} "
                f"on a {machine} machine."
            )

        })


    # ========================================================
    # SYSTEM STATUS
    # ========================================================

    if command in [

        "system status",
        "computer status",
        "pc status",
        "laptop status"

    ]:

        return jsonify({

            "receivedCommand": command,

            "action": "system_status",

            "message":
                "Your system is running normally."

        })


    # ========================================================
    # BATTERY
    # ========================================================

    if command in [

        "battery status",
        "battery level",
        "check battery",
        "battery"

    ]:

        battery = psutil.sensors_battery()


        if battery is None:

            return jsonify({

                "receivedCommand": command,

                "action":
                    "battery_status",

                "message":
                    "Battery information is "
                    "not available on this computer."

            })


        percentage = battery.percent


        if battery.power_plugged:

            message = (
                f"Your battery is at "
                f"{percentage}% and the "
                f"charger is connected."
            )

        else:

            message = (
                f"Your battery is at "
                f"{percentage}% and the "
                f"charger is not connected."
            )


        return jsonify({

            "receivedCommand": command,

            "action":
                "battery_status",

            "percentage":
                percentage,

            "powerPlugged":
                battery.power_plugged,

            "message":
                message

        })


    # ========================================================
    # CPU
    # ========================================================

    if command in [

        "cpu usage",
        "cpu status",
        "processor usage"

    ]:

        cpu_usage = psutil.cpu_percent(
            interval=1
        )


        return jsonify({

            "receivedCommand": command,

            "action":
                "cpu_status",

            "cpuUsage":
                cpu_usage,

            "message":
                f"Current CPU usage is "
                f"{cpu_usage}%."

        })


    # ========================================================
    # RAM
    # ========================================================

    if command in [

        "ram usage",
        "memory usage",
        "ram status",
        "memory status"

    ]:

        memory = psutil.virtual_memory()


        ram_usage = memory.percent

        ram_used_gb = round(
            memory.used / (1024 ** 3),
            2
        )

        ram_total_gb = round(
            memory.total / (1024 ** 3),
            2
        )


        return jsonify({

            "receivedCommand": command,

            "action":
                "ram_status",

            "ramUsage":
                ram_usage,

            "ramUsedGB":
                ram_used_gb,

            "ramTotalGB":
                ram_total_gb,

            "message": (
                f"Current RAM usage is "
                f"{ram_usage}%. "
                f"You are using "
                f"{ram_used_gb} GB out of "
                f"{ram_total_gb} GB."
            )

        })


    # ========================================================
    # DISK
    # ========================================================

    if command in [

        "disk status",
        "disk usage",
        "storage status",
        "storage usage",
        "check storage",
        "check disk"

    ]:

        disk = psutil.disk_usage(
            "C:\\"
        )


        total_gb = round(
            disk.total / (1024 ** 3),
            2
        )

        used_gb = round(
            disk.used / (1024 ** 3),
            2
        )

        free_gb = round(
            disk.free / (1024 ** 3),
            2
        )

        usage_percent = disk.percent


        return jsonify({

            "receivedCommand": command,

            "action":
                "disk_status",

            "totalGB":
                total_gb,

            "usedGB":
                used_gb,

            "freeGB":
                free_gb,

            "usagePercent":
                usage_percent,

            "message": (
                f"Your C drive is "
                f"{usage_percent}% full. "
                f"{free_gb} GB is free "
                f"out of {total_gb} GB."
            )

        })


    # ========================================================
    # INTERNET
    # ========================================================

    if command in [

        "internet status",
        "internet connection",
        "check internet",
        "network status",
        "network connection"

    ]:

        try:

            socket.create_connection(
                ("8.8.8.8", 53),
                timeout=2
            )


            return jsonify({

                "receivedCommand":
                    command,

                "action":
                    "internet_status",

                "connected":
                    True,

                "message":
                    "Your internet connection "
                    "is active."

            })


        except OSError:

            return jsonify({

                "receivedCommand":
                    command,

                "action":
                    "internet_status",

                "connected":
                    False,

                "message":
                    "Your internet connection "
                    "appears to be unavailable."

            })


    # ========================================================
    # OPEN NOTEPAD
    # ========================================================

    if command == "open notepad":

        return jsonify({

            "receivedCommand": command,

            "action":
                "open_notepad",

            "message":
                "Opening Notepad..."

        })


    # ========================================================
    # COMMAND PROMPT
    # ========================================================

    if command == "open command prompt":

        return jsonify({

            "receivedCommand": command,

            "action":
                "open_command_prompt",

            "message":
                "Opening Command Prompt..."

        })


    # ========================================================
    # FILE EXPLORER
    # ========================================================

    if command == "open file explorer":

        return jsonify({

            "receivedCommand": command,

            "action":
                "open_file_explorer",

            "message":
                "Opening File Explorer..."

        })


    # ========================================================
    # SETTINGS
    # ========================================================

    if command == "open settings":

        return jsonify({

            "receivedCommand": command,

            "action":
                "open_settings",

            "message":
                "Opening Settings..."

        })


    # ========================================================
    # TASK MANAGER
    # ========================================================

    if command == "open task manager":

        return jsonify({

            "receivedCommand": command,

            "action":
                "open_task_manager",

            "message":
                "Opening Task Manager..."

        })


    # ========================================================
    # SHUTDOWN
    # ========================================================

    if command == "shutdown computer":

        return jsonify({

            "receivedCommand": command,

            "action":
                "shutdown_confirmation",

            "message":
                "Are you sure you want to "
                "shut down the computer?"

        })


    # ========================================================
    # RESTART
    # ========================================================

    if command == "restart computer":

        return jsonify({

            "receivedCommand": command,

            "action":
                "restart_confirmation",

            "message":
                "Are you sure you want to "
                "restart the computer?"

        })


    # ========================================================
    # LOCK
    # ========================================================

    if command == "lock computer":

        return jsonify({

            "receivedCommand": command,

            "action":
                "lock_computer",

            "message":
                "Locking the computer..."

        })


    # ========================================================
    # CALCULATOR
    # ========================================================

    if command == "open calculator":

        return jsonify({

            "receivedCommand": command,

            "action":
                "open_calculator",

            "message":
                "Opening Calculator..."

        })


    # ========================================================
    # NATURAL LANGUAGE SEARCH
    # ========================================================

    search_prefixes = [

        "search ",
        "search for ",
        "please search ",
        "please search for ",
        "can you search ",
        "can you search for ",
        "google ",
        "find information about "

    ]


    for prefix in search_prefixes:

        if command.startswith(prefix):

            search_query = command[
                len(prefix):
            ].strip()


            if search_query:

                return jsonify({

                    "receivedCommand":
                        command,

                    "action":
                        "search_google",

                    "query":
                        search_query,

                    "message":
                        f"Searching Google "
                        f"for {search_query}..."

                })


    # ========================================================
    # OPEN CHROME
    # ========================================================

    if command == "open chrome":

        return jsonify({

            "receivedCommand": command,

            "action":
                "open_chrome",

            "message":
                "Opening Google Chrome..."

        })


    # ========================================================
    # OPEN YOUTUBE
    # ========================================================

    if command == "open youtube":

        return jsonify({

            "receivedCommand": command,

            "action":
                "open_youtube",

            "message":
                "Opening YouTube..."

        })


    # ========================================================
    # DEFAULT RESPONSE
    # ========================================================

    return jsonify({

        "receivedCommand":
            command,

        "action":
            "none",

        "message":
            f"Python Assistant received: "
            f"{command}"

    })


# ============================================================
# START PYTHON SERVER
# ============================================================

if __name__ == "__main__":

    print("")
    print("========================================")
    print("      VYOM ASSIST PYTHON SERVER")
    print("========================================")
    print("Server: http://127.0.0.1:5001")
    print("Health: http://127.0.0.1:5001/health")
    print("Emotion: http://127.0.0.1:5001/emotion")
    print("========================================")
    print("")


    app.run(
        host="127.0.0.1",
        port=5001
    )
