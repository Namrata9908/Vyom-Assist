from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)


# ========================================
# Common Command Normalizer
# ========================================
def normalize_command(command):

    command = command.strip().lower()

    # Normalize multiple spaces
    command = " ".join(command.split())

    # Remove common punctuation at the end
    command = command.rstrip(".!?")

    # ========================================
    # Remove common polite prefixes
    # ========================================

    prefixes_to_remove = [
        "please ",
        "can you ",
        "could you ",
        "would you ",
        "will you ",
        "kindly ",
        "hey ",
        "hey vyom ",
        "hey vyom assist ",
        "vyom ",
        "vyom assist "
    ]

    changed = True

    while changed:

        changed = False

        for prefix in prefixes_to_remove:

            if command.startswith(prefix):

                command = command[len(prefix):].strip()
                changed = True
                break


    # ========================================
    # Convert launch / start / go to / visit
    # into open
    # ========================================

    open_prefixes = [
        "launch ",
        "start ",
        "go to ",
        "visit "
    ]

    for prefix in open_prefixes:

        if command.startswith(prefix):

            command = "open " + command[len(prefix):].strip()
            break


    # ========================================
    # PC / Laptop normalization
    # ========================================

    command = command.replace("my pc", "my computer")
    command = command.replace("the pc", "the computer")

    # Standalone PC
    if command == "pc":
        command = "computer"

    # Laptop variations
    command = command.replace("my laptop", "my computer")
    command = command.replace("the laptop", "the computer")

    if command == "laptop":
        command = "computer"


    # ========================================
    # Reboot → Restart
    # ========================================

    if command.startswith("reboot "):

        command = "restart " + command[7:].strip()

    elif command == "reboot":

        command = "restart"


    # ========================================
    # Time variations
    # ========================================

    if command in [
        "what's the time",
        "whats the time",
        "tell me the time",
        "tell me what's the time",
        "tell me whats the time"
    ]:

        command = "what time is it"


    # ========================================
    # Date variations
    # ========================================

    if command in [
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


    # ========================================
    # Lock variations
    # ========================================

    if command in [
        "lock my computer",
        "lock the computer",
        "lock my pc",
        "lock the pc",
        "lock my laptop",
        "lock the laptop"
    ]:

        command = "lock computer"


    # ========================================
    # Shutdown variations
    # ========================================

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


    # ========================================
    # Restart variations
    # ========================================

    if command in [
        "restart my computer",
        "restart the computer",
        "restart my pc",
        "restart the pc",
        "restart my laptop",
        "restart the laptop"
    ]:

        command = "restart computer"


    # ========================================
    # Search variations
    # ========================================

    search_prefixes = [
        "google ",
        "search for ",
        "look up ",
        "find "
    ]

    for prefix in search_prefixes:

        if command.startswith(prefix):

            command = "search " + command[len(prefix):].strip()
            break

        

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