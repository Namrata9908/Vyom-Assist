const express = require("express");
const cors = require("cors");
const http = require("http");

const app = express();

app.use(cors());
app.use(express.json());

const PORT = 5000;

function sendToPython(command, callback) {
    const data = JSON.stringify({
        command: command
    });

    const options = {
        hostname: "127.0.0.1",
        port: 5001,
        path: "/assistant",
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(data)
        }
    };

    const request = http.request(options, (response) => {
        let body = "";

        response.on("data", (chunk) => {
            body += chunk;
        });

        response.on("end", () => {
            callback(null, body);
        });
    });

    request.on("error", (error) => {
        callback(error, null);
    });

    request.write(data);
    request.end();
}

app.get("/", (req, res) => {
    res.send("Vyom Assist Backend is running!");
});

app.get("/health", (req, res) => {
    res.json({
        status: "OK",
        message: "Vyom Assist backend is healthy"
    });
});

app.post("/assistant", (req, res) => {
    const command = req.body.command.trim().replace(/[.!?]+$/, "");

    sendToPython(command, (error, pythonResponse) => {
        if (error) {
            console.error("Python Assistant error:", error.message);

            res.status(500).json({
                receivedCommand: command,
                action: "none",
                message: "Could not connect to Python Assistant."
            });

            return;
        }

        console.log("Python response:", pythonResponse);

        const pythonData = JSON.parse(pythonResponse);

        if (pythonData.action === "greeting") {
            res.json(pythonData);
            return;
        }

        if (command.toLowerCase() === "open youtube") {
            res.json({
                receivedCommand: command,
                action: "open_youtube",
                message: "Opening YouTube..."
            });
            return;
        }

        if (command.toLowerCase() === "open google") {
            res.json({
                receivedCommand: command,
                action: "open_google",
                message: "Opening Google..."
            });
            return;
        }

        if (command.toLowerCase() === "open gmail") {
            res.json({
                receivedCommand: command,
                action: "open_gmail",
                message: "Opening Gmail..."
            });
            return;
        }

        if (command.toLowerCase().startsWith("search ")) {
            const searchQuery = command.substring(7).trim();

            res.json({
                receivedCommand: command,
                action: "search_google",
                query: searchQuery,
                message: `Searching Google for ${searchQuery}...`
            });
            return;
        }

        res.json({
            receivedCommand: command,
            action: "none",
            message: `Vyom Assist received your command: ${command}`
        });
    });
});

app.listen(PORT, () => {
    console.log(`Vyom Assist Backend running on http://localhost:${PORT}`);
});