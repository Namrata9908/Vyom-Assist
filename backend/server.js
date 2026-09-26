const express = require("express");
const cors = require("cors");
const http = require("http");
const { exec } = require("child_process");

const app = express();

app.use(cors());
app.use(express.json());

const PORT = 5000;


// ===============================
// Send command to Python Assistant
// ===============================

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


// ===============================
// Home
// ===============================

app.get("/", (req, res) => {

    res.send("Vyom Assist Backend is running!");

});


// ===============================
// Health Check
// ===============================

app.get("/health", (req, res) => {

    res.json({
        status: "OK",
        message: "Vyom Assist backend is healthy"
    });

});


// ===============================
// Shutdown Computer
// ===============================

app.post("/shutdown", (req, res) => {

    exec("shutdown /s /t 0");

    res.json({
        status: "success",
        message: "Computer is shutting down..."
    });

});


// ===============================
// Restart Computer
// ===============================

app.post("/restart", (req, res) => {

    exec("shutdown /r /t 0");

    res.json({
        status: "success",
        message: "Computer is restarting..."
    });

});


// ===============================
// Main Assistant Endpoint
// ===============================

app.post("/assistant", (req, res) => {

    const command = req.body.command.trim().replace(/[.!?]+$/, "");


    sendToPython(command, (error, pythonResponse) => {

        // ===============================
        // Python connection error
        // ===============================

        if (error) {

            console.error(
                "Python Assistant error:",
                error.message
            );

            res.status(500).json({
                receivedCommand: command,
                action: "none",
                message: "Could not connect to Python Assistant."
            });

            return;
        }


        console.log(
            "Python response:",
            pythonResponse
        );


        const pythonData = JSON.parse(pythonResponse);


        // ===============================
        // Greeting
        // ===============================

        if (pythonData.action === "greeting") {

            res.json(pythonData);

            return;
        }


        // ===============================
        // Time
        // ===============================

        if (pythonData.action === "time") {

            res.json(pythonData);

            return;
        }


        // ===============================
        // Date
        // ===============================

        if (pythonData.action === "date") {

            res.json(pythonData);

            return;
        }


        // ===============================
        // Open Calculator
        // ===============================

        if (pythonData.action === "open_calculator") {

            exec("start calc");

            res.json(pythonData);

            return;
        }


        // ===============================
        // Open Notepad
        // ===============================

        if (pythonData.action === "open_notepad") {

            exec("start notepad");

            res.json(pythonData);

            return;
        }


        // ===============================
        // Open Command Prompt
        // ===============================

        if (pythonData.action === "open_command_prompt") {

            exec("start cmd");

            res.json(pythonData);

            return;
        }


        // ===============================
        // Open Task Manager
        // ===============================

        if (pythonData.action === "open_task_manager") {

            exec("start taskmgr");

            res.json(pythonData);

            return;
        }


        // ===============================
        // Shutdown Confirmation
        // ===============================

        if (pythonData.action === "shutdown_confirmation") {

            res.json(pythonData);

            return;
        }


        // ===============================
        // Restart Confirmation
        // ===============================

        if (pythonData.action === "restart_confirmation") {

            res.json(pythonData);

            return;
        }

        // ===============================
        // Lock Computer
        // ===============================

        if (pythonData.action === "lock_computer") {

            exec("rundll32.exe user32.dll,LockWorkStation");

            res.json(pythonData);

            return;
        }

        // ===============================
        // Open File Explorer
        // ===============================

        if (pythonData.action === "open_file_explorer") {

            exec("start explorer");

            res.json(pythonData);

            return;
        }


        // ===============================
        // Open Settings
        // ===============================

        if (pythonData.action === "open_settings") {

            exec("start ms-settings:");

            res.json(pythonData);

            return;
        }


        // ===============================
        // Open Chrome
        // ===============================

        if (pythonData.action === "open_chrome") {

            exec("start chrome");

            res.json(pythonData);

            return;
        }

        // ===============================
        // Open YouTube
        // ===============================

        if (command.toLowerCase() === "open youtube") {

            res.json({

                receivedCommand: command,

                action: "open_youtube",

                message: "Opening YouTube..."

            });

            return;
        }


        // ===============================
        // Open Google
        // ===============================

        if (command.toLowerCase() === "open google") {

            res.json({

                receivedCommand: command,

                action: "open_google",

                message: "Opening Google..."

            });

            return;
        }


        // ===============================
        // Open Gmail
        // ===============================

        if (command.toLowerCase() === "open gmail") {

            res.json({

                receivedCommand: command,

                action: "open_gmail",

                message: "Opening Gmail..."

            });

            return;
        }


        // ===============================
        // Google Search
        // ===============================

        if (command.toLowerCase().startsWith("search ")) {

            const searchQuery =
                command.substring(7).trim();


            res.json({

                receivedCommand: command,

                action: "search_google",

                query: searchQuery,

                message:
                    `Searching Google for ${searchQuery}...`

            });

            return;
        }

        // ===============================
        // Open Any Website
        // ===============================

        if (command.toLowerCase().startsWith("open ")) {

            const websiteName = command.substring(5).trim();

            const websiteUrl = `https://www.${websiteName}.com`;

            res.json({
                receivedCommand: command,
                action: "open_website",
                website: websiteName,
                url: websiteUrl,
                message: `Opening ${websiteName}...`
            });

            return;
        }

        // ===============================
        // Default Response
        // ===============================

        res.json({

            receivedCommand: command,

            action: "none",

            message:
                `Vyom Assist received your command: ${command}`

        });

    });

});


// ===============================
// Start Server
// ===============================

app.listen(PORT, () => {

    console.log(
        `Vyom Assist Backend running on http://localhost:${PORT}`
    );

});