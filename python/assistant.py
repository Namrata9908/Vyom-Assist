from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return "Vyom Assist Python Assistant is running!"


@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "message": "Python assistant is healthy"
    })

@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.get_json()
    command = data.get("command", "").strip().lower()

    if command == "hello":
     return jsonify({
        "receivedCommand": command,
        "action": "greeting",
        "message": "Hello! I am Vyom Assist. How can I help you?"
    })

    if command == "hi":
     return jsonify({
        "receivedCommand": command,
        "action": "greeting",
        "message": "Hi! I am Vyom Assist. How can I help you?"
    })

    if command == "how are you":
     return jsonify({
        "receivedCommand": command,
        "action": "greeting",
        "message": "I am doing great! How can I help you?"
    })

    if command == "what is your name":
     return jsonify({
        "receivedCommand": command,
        "action": "greeting",
        "message": "My name is Vyom Assist."
    })

    if command == "what time is it":
     current_time = datetime.now().strftime("%I:%M %p")

     return jsonify({
        "receivedCommand": command,
        "action": "time",
        "message": f"The current time is {current_time}."
    })

    if command == "what is today's date":
     current_date = datetime.now().strftime("%d %B %Y")

     return jsonify({
        "receivedCommand": command,
        "action": "date",
        "message": f"Today's date is {current_date}."
    })

    if command == "open notepad":
     return jsonify({
        "receivedCommand": command,
        "action": "open_notepad",
        "message": "Opening Notepad..."
    })


    if command == "open command prompt":
        return jsonify({
            "receivedCommand": command,
            "action": "open_command_prompt",
            "message": "Opening Command Prompt..."
        })

    if command == "open file explorer":
        return jsonify({
            "receivedCommand": command,
            "action": "open_file_explorer",
            "message": "Opening File Explorer..."
        })

    if command == "open settings":
        return jsonify({
            "receivedCommand": command,
            "action": "open_settings",
            "message": "Opening Settings..."
        })

    if command == "open task manager":
        return jsonify({
            "receivedCommand": command,
            "action": "open_task_manager",
            "message": "Opening Task Manager..."
        })

    if command == "shutdown computer":
        return jsonify({
            "receivedCommand": command,
            "action": "shutdown_confirmation",
            "message": "Are you sure you want to shut down the computer?"
        })

    if command == "restart computer":
     return jsonify({
        "receivedCommand": command,
        "action": "restart_confirmation",
        "message": "Are you sure you want to restart the computer?"
    })
    
    if command == "open calculator":
     return jsonify({
        "receivedCommand": command,
        "action": "open_calculator",
        "message": "Opening Calculator..."
    })



    if command == "open youtube":
        return jsonify({
            "receivedCommand": command,
            "action": "open_youtube",
            "message": "Opening YouTube..."
        })

    return jsonify({
        "receivedCommand": command,
        "action": "none",
        "message": f"Python Assistant received: {command}"
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)