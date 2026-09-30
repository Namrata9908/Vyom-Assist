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


// ========================================
// Start Button
// ========================================

startButton.addEventListener("click", function () {

    alert("Vyom Assist is ready!");

});


// ========================================
// Send Command
// ========================================

sendCommandButton.addEventListener("click", async function () {

    const command = commandInput.value.trim();

    if (command === "") {

        alert("Please enter a command.");

        return;
    }


    try {

        const response = await fetch(
            "http://localhost:5000/assistant",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    command: command
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                `Backend returned ${response.status}`
            );

        }


        const data = await response.json();


        console.log("Vyom Assist response:", data);


        // ========================================
        // Shutdown Confirmation
        // ========================================

        if (data.action === "shutdown_confirmation") {

            shutdownModal.style.display = "flex";

            return;
        }


        // ========================================
        // Restart Confirmation
        // ========================================

        else if (data.action === "restart_confirmation") {

            restartModal.style.display = "flex";

            return;
        }


        // ========================================
        // Lock Computer
        // ========================================

        else if (data.action === "lock_computer") {

            alert(data.message);

            return;
        }


        // ========================================
        // Greeting
        // ========================================

        else if (data.action === "greeting") {

            alert(data.message);

            return;
        }


        // ========================================
        // Time
        // ========================================

        else if (data.action === "time") {

            alert(data.message);

            return;
        }


        // ========================================
        // Date
        // ========================================

        else if (data.action === "date") {

            alert(data.message);

            return;
        }


        // ========================================
        // Calculator
        // ========================================

        else if (data.action === "open_calculator") {

            alert(data.message);

            return;
        }


        // ========================================
        // Chrome
        // ========================================

        else if (data.action === "open_chrome") {

            alert(data.message);

            return;
        }


        // ========================================
        // YouTube
        // ========================================

        else if (data.action === "open_youtube") {

            window.open(
                "https://www.youtube.com",
                "_blank"
            );

            return;
        }


        // ========================================
        // Google
        // ========================================

        else if (data.action === "open_google") {

            window.open(
                "https://www.google.com",
                "_blank"
            );

            return;
        }


        // ========================================
        // Gmail
        // ========================================

        else if (data.action === "open_gmail") {

            window.open(
                "https://mail.google.com",
                "_blank"
            );

            return;
        }


        // ========================================
        // Generic Website
        // ========================================

        else if (data.action === "open_website") {

            let website = data.website.trim();


            if (
                website.startsWith("http://") ||
                website.startsWith("https://")
            ) {

                window.open(
                    website,
                    "_blank"
                );

            }

            else if (website.includes(".")) {

                window.open(
                    "https://" + website,
                    "_blank"
                );

            }

            else {

                window.open(
                    "https://www." + website + ".com",
                    "_blank"
                );

            }

            return;
        }


        // ========================================
        // Google Search
        // ========================================

        else if (data.action === "search_google") {

            const searchUrl =
                "https://www.google.com/search?q=" +
                encodeURIComponent(data.query);


            window.open(
                searchUrl,
                "_blank"
            );

            return;
        }


        // ========================================
        // Default Response
        // ========================================

        else {

            alert(data.message);

            return;
        }

    }

    catch (error) {

        console.error(
            "Vyom Assist frontend error:",
            error
        );

        alert(
            "Could not connect to Vyom Assist backend."
        );

    }

});


// ========================================
// Voice Button
// ========================================

voiceButton.addEventListener("click", function () {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Speech recognition is not supported in this browser."
        );

        return;
    }


    const recognition =
        new SpeechRecognition();


    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;

    voiceButton.textContent = "🎤 Listening...";
    voiceButton.disabled = true;

    recognition.start();


    voiceButton.textContent =
        "🎙️ Listening...";


    recognition.onresult = function (event) {

        const spokenCommand =
            event.results[0][0].transcript;

        commandInput.value =
            spokenCommand;

        voiceButton.textContent =
            "🎤 Speak Command";

        // Automatically send the voice command
        sendCommandButton.click();
    };


    recognition.onerror = (event) => {
        if (event.error === "no-speech") {
            return;
        }

        if (event.error === "not-allowed") {
            alert("Microphone permission is required.");
            return;
        }

        alert("Voice recognition error. Please try again.");
    };


    recognition.onend = function () {

        voiceButton.textContent = "🎤 Speak Command";
        voiceButton.disabled = false;

    };

});


// ========================================
// Shutdown - Yes Button
// ========================================

shutdownYesButton.addEventListener(
    "click",
    async () => {

        const finalConfirm = confirm(
            "Final confirmation: Do you really want to shut down this computer?"
        );


        if (!finalConfirm) {

            shutdownModal.style.display =
                "none";

            return;
        }


        shutdownModal.style.display =
            "none";


        try {

            const response = await fetch(
                "http://localhost:5000/shutdown",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    }
                }
            );


            const data =
                await response.json();


            alert(data.message);

        }

        catch (error) {

            console.error(error);

            alert(
                "Could not connect to Vyom Assist backend."
            );

        }

    }
);


// ========================================
// Shutdown - No Button
// ========================================

shutdownNoButton.addEventListener(
    "click",
    () => {

        shutdownModal.style.display =
            "none";

    }
);


// ========================================
// Restart - Yes Button
// ========================================

restartYesButton.addEventListener(
    "click",
    async () => {

        const finalConfirm = confirm(
            "Final confirmation: Do you really want to restart this computer?"
        );


        if (!finalConfirm) {

            restartModal.style.display =
                "none";

            return;
        }


        restartModal.style.display =
            "none";


        try {

            const response = await fetch(
                "http://localhost:5000/restart",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    }
                }
            );


            const data =
                await response.json();


            console.log(data);


            alert(data.message);

        }

        catch (error) {

            console.error(error);

            alert(
                "Could not connect to Vyom Assist backend."
            );

        }

    }
);


// ========================================
// Restart - No Button
// ========================================

restartNoButton.addEventListener(
    "click",
    () => {

        restartModal.style.display =
            "none";

    }
);