from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)


# ========================================
# Common Command Normalizer
# ========================================

def normalize_command(command):

    command = command.strip().lower()

    # Remove common polite prefixes
    prefixes_to_remove = [
        "please ",
        "can you ",
        "could you ",
        "would you ",
        "will you "
    ]

    for prefix in prefixes_to_remove:

        if command.startswith(prefix):
            command = command[len(prefix):].strip()
            break

    # Convert launch/start into open
    if command.startswith("launch "):
        command = "open " + command[7:].strip()

    elif command.startswith("start "):
        command = "open " + command[6:].strip()

    return command


# ========================================
# Home
# ========================================

@app.route("/")
def home():
    return "Vyom Assist Python Assistant is running!"


# ========================================
# Health Check
# ========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "OK",
        "message": "Python assistant is healthy"
    })


# ========================================
# Assistant
# ========================================

@app.route("/assistant", methods=["POST"])
def assistant():

    data = request.get_json() or {}

    command = normalize_command(
        data.get("command", "")
    )


    # ========================================
    # Hello
    # ========================================

    if command == "hello":

        return jsonify({
            "receivedCommand": command,
            "action": "greeting",
            "message": "Hello! I am Vyom Assist. How can I help you?"
        })


    # ========================================
    # Hi
    # ========================================

    if command == "hi":

        return jsonify({
            "receivedCommand": command,
            "action": "greeting",
            "message": "Hi! I am Vyom Assist. How can I help you?"
        })


    # ========================================
    # How are you
    # ========================================

    if command == "how are you":

        return jsonify({
            "receivedCommand": command,
            "action": "greeting",
            "message": "I am doing great! How can I help you?"
        })


    # ========================================
    # Name
    # ========================================

    if command == "what is your name":

        return jsonify({
            "receivedCommand": command,
            "action": "greeting",
            "message": "My name is Vyom Assist."
        })


    # ========================================
    # Time
    # ========================================

    if command == "what time is it":

        current_time = datetime.now().strftime("%I:%M %p")

        return jsonify({
            "receivedCommand": command,
            "action": "time",
            "message": f"The current time is {current_time}."
        })


    # ========================================
    # Date
    # ========================================

    if command == "what is today's date":

        current_date = datetime.now().strftime("%d %B %Y")

        return jsonify({
            "receivedCommand": command,
            "action": "date",
            "message": f"Today's date is {current_date}."
        })


    # ========================================
    # Open Notepad
    # ========================================

    if command == "open notepad":

        return jsonify({
            "receivedCommand": command,
            "action": "open_notepad",
            "message": "Opening Notepad..."
        })


    # ========================================
    # Open Command Prompt
    # ========================================

    if command == "open command prompt":

        return jsonify({
            "receivedCommand": command,
            "action": "open_command_prompt",
            "message": "Opening Command Prompt..."
        })


    # ========================================
    # Open File Explorer
    # ========================================

    if command == "open file explorer":

        return jsonify({
            "receivedCommand": command,
            "action": "open_file_explorer",
            "message": "Opening File Explorer..."
        })


    # ========================================
    # Open Settings
    # ========================================

    if command == "open settings":

        return jsonify({
            "receivedCommand": command,
            "action": "open_settings",
            "message": "Opening Settings..."
        })


    # ========================================
    # Open Task Manager
    # ========================================

    if command == "open task manager":

        return jsonify({
            "receivedCommand": command,
            "action": "open_task_manager",
            "message": "Opening Task Manager..."
        })


    # ========================================
    # Shutdown Computer
    # ========================================

    if command == "shutdown computer":

        return jsonify({
            "receivedCommand": command,
            "action": "shutdown_confirmation",
            "message": "Are you sure you want to shut down the computer?"
        })


    # ========================================
    # Restart Computer
    # ========================================

    if command == "restart computer":

        return jsonify({
            "receivedCommand": command,
            "action": "restart_confirmation",
            "message": "Are you sure you want to restart the computer?"
        })


    # ========================================
    # Lock Computer
    # ========================================

    if command == "lock computer":

        return jsonify({
            "receivedCommand": command,
            "action": "lock_computer",
            "message": "Locking the computer..."
        })


    # ========================================
    # Open Calculator
    # ========================================

    if command == "open calculator":

        return jsonify({
            "receivedCommand": command,
            "action": "open_calculator",
            "message": "Opening Calculator..."
        })


    # ========================================
    # Natural Language Search
    # ========================================

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

            search_query = command[len(prefix):].strip()

            if search_query:

                return jsonify({
                    "receivedCommand": command,
                    "action": "search_google",
                    "query": search_query,
                    "message": f"Searching Google for {search_query}..."
                })


    # ========================================
    # Open Chrome
    # ========================================

    if command == "open chrome":

        return jsonify({
            "receivedCommand": command,
            "action": "open_chrome",
            "message": "Opening Google Chrome..."
        })


    # ========================================
    # Open YouTube
    # ========================================

    if command == "open youtube":

        return jsonify({
            "receivedCommand": command,
            "action": "open_youtube",
            "message": "Opening YouTube..."
        })


    # ========================================
    # Default Response
    # ========================================

    return jsonify({
        "receivedCommand": command,
        "action": "none",
        "message": f"Python Assistant received: {command}"
    })


# ========================================
# Start Python Server
# ========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5001
    )