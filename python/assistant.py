from flask import Flask, jsonify, request

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