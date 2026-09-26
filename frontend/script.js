const startButton = document.getElementById("startButton");
const commandInput = document.getElementById("commandInput");
const sendCommandButton = document.getElementById("sendCommandButton");
const voiceButton = document.getElementById("voiceButton");
const shutdownModal = document.getElementById("shutdownModal");
const shutdownYesButton = document.getElementById("shutdownYesButton");
const shutdownNoButton = document.getElementById("shutdownNoButton");
const restartModal = document.getElementById("restartModal");
const restartYesButton = document.getElementById("restartYesButton");
const restartNoButton = document.getElementById("restartNoButton");

startButton.addEventListener("click", function () {
    alert("Vyom Assist is ready!");
});

sendCommandButton.addEventListener("click", async function () {
    const command = commandInput.value;

    if (command.trim() === "") {
        alert("Please enter a command.");
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/assistant", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: command
            })
        });

        const data = await response.json();

        if (data.action === "shutdown_confirmation") {
            shutdownModal.style.display = "flex";
            return;
        } else if (data.action === "restart_confirmation") {
            restartModal.style.display = "flex";
            return;
        } else if (data.action === "greeting") {
            alert(data.message);
        } else if (data.action === "time") {
            alert(data.message);
        } else if (data.action === "open_calculator") {
            alert(data.message);
        } else if (data.action === "open_youtube") {
            window.open("https://www.youtube.com", "_blank");
        } else if (data.action === "open_google") {
            window.open("https://www.google.com", "_blank");
        } else if (data.action === "open_gmail") {
            window.open("https://mail.google.com", "_blank");
        } else if (data.action === "search_google") {
            const searchUrl =
                "https://www.google.com/search?q=" +
                encodeURIComponent(data.query);

            window.open(searchUrl, "_blank");
        } else {
            alert(data.message);
        }

    } catch (error) {
        alert("Could not connect to Vyom Assist backend.");
        console.error(error);
    }
});

voiceButton.addEventListener("click", function () {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Speech recognition is not supported in this browser.");
        return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.start();

    voiceButton.textContent = "🎙️ Listening...";

    recognition.onresult = function (event) {
        const spokenCommand = event.results[0][0].transcript;

        commandInput.value = spokenCommand;

        voiceButton.textContent = "🎤 Speak Command";
    };

    recognition.onerror = function (event) {
        console.error("Speech recognition error:", event.error);

        voiceButton.textContent = "🎤 Speak Command";

        alert("Could not recognize your voice.");
    };

    recognition.onend = function () {
        voiceButton.textContent = "🎤 Speak Command";
    };
});

shutdownYesButton.addEventListener("click", async () => {

    const finalConfirm = confirm(
        "Final confirmation: Do you really want to shut down this computer?"
    );

    if (!finalConfirm) {
        shutdownModal.style.display = "none";
        return;
    }
    shutdownModal.style.display = "none";

    try {
        const response = await fetch("http://localhost:5000/shutdown", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();
        alert(data.message);
    } catch (error) {
        alert("Could not connect to Vyom Assist backend.");
    }
});

shutdownNoButton.addEventListener("click", () => {
    shutdownModal.style.display = "none";
});

restartYesButton.addEventListener("click", async () => {

    const finalConfirm = confirm(
        "Final confirmation: Do you really want to restart this computer?"
    );

    if (!finalConfirm) {
        restartModal.style.display = "none";
        return;
    }

    restartModal.style.display = "none";

    try {

        const response = await fetch("http://localhost:5000/restart", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        console.log(data);

        alert(data.message);

    } catch (error) {

        console.error(error);

        alert("Could not connect to Vyom Assist backend.");

    }
});

restartNoButton.addEventListener("click", () => {
    restartModal.style.display = "none";
});