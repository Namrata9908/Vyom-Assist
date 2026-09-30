const express = require("express");
const cors = require("cors");
const http = require("http");
const { exec } = require("child_process");

const app = express();

app.use(cors());
app.use(express.json());

const PORT = 5000;


// ========================================
// Command Normalizer
// ========================================

function normalizeCommand(command) {

    command = command.trim().toLowerCase();

    // Normalize multiple spaces
    command = command.replace(/\s+/g, " ");

    // Remove common punctuation
    command = command.replace(/[.!?]+$/, "");


    // Remove common polite prefixes
    const prefixesToRemove = [
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
    ];

    let changed = true;

    while (changed) {

        changed = false;

        for (const prefix of prefixesToRemove) {

            if (command.startsWith(prefix)) {

                command = command.substring(
                    prefix.length
                ).trim();

                changed = true;

                break;
            }
        }
    }


    // ========================================
    // Convert common OPEN variations
    // ========================================

    const openPrefixes = [
        "launch ",
        "start ",
        "go to ",
        "visit "
    ];

    for (const prefix of openPrefixes) {

        if (command.startsWith(prefix)) {

            command =
                "open " +
                command.substring(prefix.length).trim();

            break;
        }
    }


    // ========================================
    // Convert common TIME variations
    // ========================================

    if (
        command === "what's the time" ||
        command === "whats the time" ||
        command === "tell me the time" ||
        command === "can you tell me the time"
    ) {
        command = "what time is it";
    }


    // ========================================
    // Convert common DATE variations
    // ========================================

    if (
        command === "what's today's date" ||
        command === "what’s today's date" ||
        command === "what's today’s date" ||
        command === "what’s today’s date" ||
        command === "whats today's date" ||
        command === "tell me today's date" ||
        command === "tell me today’s date" ||
        command === "tell me todays date"
    ) {
        command = "what is today's date";
    }


    // ========================================
    // Convert common LOCK variations
    // ========================================

    if (
        command === "lock my computer" ||
        command === "lock the computer"
    ) {
        command = "lock computer";
    }


    // ========================================
    // Convert common SHUTDOWN variations
    // ========================================

    if (
        command === "shutdown my computer" ||
        command === "shutdown the computer"
    ) {
        command = "shutdown computer";
    }


    // ========================================
    // Convert common SHUT DOWN variations
    // ========================================

    if (
        command === "shut down my computer" ||
        command === "shut down the computer"
    ) {
        command = "shutdown computer";
    }


    // ========================================
    // Convert common RESTART variations
    // ========================================

    if (
        command === "restart my computer" ||
        command === "restart the computer"
    ) {
        command = "restart computer";
    }


    // ========================================
    // Convert common SEARCH variations
    // ========================================

    const searchPrefixes = [
        "google ",
        "search for ",
        "look up ",
        "find "
    ];

    for (const prefix of searchPrefixes) {

        if (command.startsWith(prefix)) {

            command =
                "search " +
                command.substring(prefix.length).trim();

            break;
        }
    }


    // PC / laptop / reboot variations
    command = command
        .replace(/\bmy pc\b/g, "my computer")
        .replace(/\bthe pc\b/g, "the computer")
        .replace(/\bpc\b/g, "computer")
        .replace(/\blaptop\b/g, "computer")
        .replace(/\breboot\b/g, "restart");


    // ========================================
    // Direct Website / URL Commands
    // ========================================

    const validDomainPattern =
        /^(?:[a-zA-Z0-9-]+\.)+(com|org|net|in|co\.in|io|dev|ai|app|edu|gov)(\/.*)?$/;

    if (
        command.startsWith("http://") ||
        command.startsWith("https://")
    ) {
        command = "open " + command;
    }
    else if (validDomainPattern.test(command)) {
        command = "open " + command;
    }

    return command;
}


// ========================================
// Send command to Python Assistant
// ========================================

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


// ========================================
// Home
// ========================================

app.get("/", (req, res) => {

    res.send("Vyom Assist Backend is running!");

});


// ========================================
// Health Check
// ========================================

app.get("/health", (req, res) => {

    res.json({
        status: "OK",
        message: "Vyom Assist backend is healthy"
    });

});


// ========================================
// Shutdown Computer
// ========================================

app.post("/shutdown", (req, res) => {

    exec("shutdown /s /t 0");

    res.json({
        status: "success",
        message: "Computer is shutting down..."
    });

});


// ========================================
// Restart Computer
// ========================================

app.post("/restart", (req, res) => {

    exec("shutdown /r /t 0");

    res.json({
        status: "success",
        message: "Computer is restarting..."
    });

});


// ========================================
// Main Assistant Endpoint
// ========================================

app.post("/assistant", (req, res) => {

    const command = normalizeCommand(
        req.body.command || ""
    );

    sendToPython(command, (error, pythonResponse) => {


        // ========================================
        // Python connection error
        // ========================================

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


        // ========================================
        // Greeting
        // ========================================

        if (pythonData.action === "greeting") {

            res.json(pythonData);

            return;
        }


        // ========================================
        // Time
        // ========================================

        if (pythonData.action === "time") {

            res.json(pythonData);

            return;
        }


        // ========================================
        // Date
        // ========================================

        if (pythonData.action === "date") {

            res.json(pythonData);

            return;
        }

        // ========================================
        // System Information
        // ========================================

        if (pythonData.action === "system_info") {

            res.json(pythonData);

            return;
        }

        // ========================================
        // System Status
        // ========================================

        if (pythonData.action === "system_status") {

            res.json(pythonData);

            return;
        }

        // ========================================
        // Battery Status
        // ========================================

        if (pythonData.action === "battery_status") {

            res.json(pythonData);

            return;
        }

        // ========================================
        // CPU Status
        // ========================================

        if (pythonData.action === "cpu_status") {

            res.json(pythonData);

            return;
        }

        // ========================================
        // RAM Status
        // ========================================

        if (pythonData.action === "ram_status") {

            res.json(pythonData);

            return;
        }

        // ========================================
        // Disk / Storage Status
        // ========================================

        if (pythonData.action === "disk_status") {

            res.json(pythonData);

            return;
        }

        // ========================================
        // Internet / Network Status
        // ========================================

        if (pythonData.action === "internet_status") {

            res.json(pythonData);

            return;
        }

        // ========================================
        // Search from Python
        // ========================================

        if (pythonData.action === "search_google") {

            res.json(pythonData);

            return;
        }


        // ========================================
        // Open Calculator
        // ========================================

        if (pythonData.action === "open_calculator") {

            exec("start calc");

            res.json(pythonData);

            return;
        }


        // ========================================
        // Open Notepad
        // ========================================

        if (pythonData.action === "open_notepad") {

            exec("start notepad");

            res.json(pythonData);

            return;
        }


        // ========================================
        // Open Command Prompt
        // ========================================

        if (pythonData.action === "open_command_prompt") {

            exec("start cmd");

            res.json(pythonData);

            return;
        }


        // ========================================
        // Open Task Manager
        // ========================================

        if (pythonData.action === "open_task_manager") {

            exec("start taskmgr");

            res.json(pythonData);

            return;
        }


        // ========================================
        // Shutdown Confirmation
        // ========================================

        if (pythonData.action === "shutdown_confirmation") {

            res.json(pythonData);

            return;
        }


        // ========================================
        // Restart Confirmation
        // ========================================

        if (pythonData.action === "restart_confirmation") {

            res.json(pythonData);

            return;
        }


        // ========================================
        // Lock Computer
        // ========================================

        if (pythonData.action === "lock_computer") {

            exec(
                "rundll32.exe user32.dll,LockWorkStation"
            );

            res.json(pythonData);

            return;
        }


        // ========================================
        // Open File Explorer
        // ========================================

        if (pythonData.action === "open_file_explorer") {

            exec("start explorer");

            res.json(pythonData);

            return;
        }


        // ========================================
        // Open Settings
        // ========================================

        if (pythonData.action === "open_settings") {

            exec("start ms-settings:");

            res.json(pythonData);

            return;
        }


        // ========================================
        // Open Chrome
        // ========================================

        if (pythonData.action === "open_chrome") {

            exec("start chrome");

            res.json(pythonData);

            return;
        }


        // ========================================
        // Open YouTube
        // ========================================

        if (command === "open youtube") {

            res.json({

                receivedCommand: command,

                action: "open_youtube",

                message: "Opening YouTube..."

            });

            return;
        }


        // ========================================
        // Open Google
        // ========================================

        if (command === "open google") {

            res.json({

                receivedCommand: command,

                action: "open_google",

                message: "Opening Google..."

            });

            return;
        }


        // ========================================
        // Open Gmail
        // ========================================

        if (command === "open gmail") {

            res.json({

                receivedCommand: command,

                action: "open_gmail",

                message: "Opening Gmail..."

            });

            return;
        }


        // ========================================
        // Google Search
        // ========================================

        if (command.startsWith("search ")) {

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


        // ========================================
        // Open Any Website - Smart
        // ========================================

        if (command.startsWith("open ")) {

            const websiteName =
                command.substring(5).trim();


            if (websiteName !== "") {

                let websiteUrl;


                // Complete URL
                if (
                    websiteName.startsWith("http://") ||
                    websiteName.startsWith("https://")
                ) {

                    websiteUrl = websiteName;

                }


                // Domain like github.com
                else if (websiteName.includes(".")) {

                    websiteUrl =
                        `https://${websiteName}`;

                }


                // Assume .com
                else {

                    websiteUrl =
                        `https://www.${websiteName}.com`;

                }


                res.json({

                    receivedCommand: command,

                    action: "open_website",

                    website: websiteName,

                    url: websiteUrl,

                    message:
                        `Opening ${websiteName}...`

                });

                return;
            }
        }


        // ========================================
        // Default Response
        // ========================================

        res.json({

            receivedCommand: command,

            action: "none",

            message:
                `Vyom Assist received your command: ${command}`

        });

    });

});


// ========================================
// Start Server
// ========================================

app.listen(PORT, () => {

    console.log(
        `Vyom Assist Backend running on http://localhost:${PORT}`
    );

});