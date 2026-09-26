const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

const PORT = 5000;

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

app.listen(PORT, () => {
    console.log(`Vyom Assist Backend running on http://localhost:${PORT}`);
});