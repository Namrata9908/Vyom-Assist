from flask import Flask, jsonify

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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)