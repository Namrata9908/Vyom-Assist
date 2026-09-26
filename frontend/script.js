const startButton = document.getElementById("startButton");
const commandInput = document.getElementById("commandInput");
const sendCommandButton = document.getElementById("sendCommandButton");
const voiceButton = document.getElementById("voiceButton");

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

        if (data.action === "open_youtube") {
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