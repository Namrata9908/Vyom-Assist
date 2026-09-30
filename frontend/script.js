// ========================================
// DOM Elements
// ========================================

const startButton =
    document.getElementById("startButton");

const responseBox =
    document.getElementById("responseBox");

const responseMessage =
    document.getElementById("responseMessage");

const commandInput =
    document.getElementById("commandInput");

const sendCommandButton =
    document.getElementById("sendCommandButton");

const voiceButton =
    document.getElementById("voiceButton");


// Shutdown

const shutdownModal =
    document.getElementById("shutdownModal");

const shutdownYesButton =
    document.getElementById("shutdownYesButton");

const shutdownNoButton =
    document.getElementById("shutdownNoButton");


// Restart

const restartModal =
    document.getElementById("restartModal");

const restartYesButton =
    document.getElementById("restartYesButton");

const restartNoButton =
    document.getElementById("restartNoButton");


// History

const historyList =
    document.getElementById("historyList");

const clearHistoryButton =
    document.getElementById("clearHistoryButton");


// ========================================
// Show Assistant Response
// ========================================

function showResponse(message) {

    responseMessage.textContent =
        message || "Command processed.";

}


// ========================================
// Processing Indicator
// ========================================

function showProcessing() {

    showResponse(
        "⏳ Vyom Assist is processing..."
    );

}


// ========================================
// Command History
// ========================================

function addToHistory(command, response) {

    // Remove empty message

    const emptyMessage =
        historyList.querySelector(
            ".empty-history"
        );


    if (emptyMessage) {

        emptyMessage.remove();

    }


    // Create history item

    const historyItem =
        document.createElement("div");


    historyItem.className =
        "history-item";


    // ========================================
    // User Command
    // ========================================

    const commandLine =
        document.createElement("div");


    const commandLabel =
        document.createElement("strong");


    commandLabel.textContent =
        "You: ";


    const commandText =
        document.createElement("span");


    commandText.textContent =
        command;


    commandLine.appendChild(
        commandLabel
    );


    commandLine.appendChild(
        commandText
    );


    // ========================================
    // Assistant Response
    // ========================================

    const responseLine =
        document.createElement("div");


    const responseLabel =
        document.createElement("strong");


    responseLabel.textContent =
        "Vyom Assist: ";


    const responseText =
        document.createElement("span");


    responseText.textContent =
        response;


    responseLine.appendChild(
        responseLabel
    );


    responseLine.appendChild(
        responseText
    );


    // ========================================
    // Add to History
    // ========================================

    historyItem.appendChild(
        commandLine
    );


    historyItem.appendChild(
        responseLine
    );


    // Newest command at top

    historyList.prepend(
        historyItem
    );

}


// ========================================
// Clear Command History
// ========================================

clearHistoryButton.addEventListener(
    "click",
    function () {

        const hasHistory =
            historyList.querySelector(
                ".history-item"
            );


        if (!hasHistory) {

            showResponse(
                "Command history is already empty."
            );

            return;

        }


        const confirmed =
            confirm(
                "Are you sure you want to clear command history?"
            );


        if (!confirmed) {

            return;

        }


        historyList.innerHTML = `
            <p class="empty-history">
                No commands yet.
            </p>
        `;


        showResponse(
            "Command history cleared."
        );

    }
);


// ========================================
// Start Assistant
// ========================================

startButton.addEventListener(
    "click",
    function () {

        showResponse(
            "Vyom Assist is ready!"
        );

    }
);


// ========================================
// Send Command
// ========================================

sendCommandButton.addEventListener(
    "click",
    async function () {

        const command =
            commandInput.value.trim();


        // ========================================
        // Empty Command
        // ========================================

        if (command === "") {

            showResponse(
                "Please enter a command."
            );

            return;

        }


        // ========================================
        // Processing
        // ========================================

        showProcessing();


        sendCommandButton.disabled =
            true;


        try {

            const response =
                await fetch(
                    "http://localhost:5000/assistant",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            command: command
                        })
                    }
                );


            // ========================================
            // Backend Error
            // ========================================

            if (!response.ok) {

                throw new Error(
                    `Backend returned ${response.status}`
                );

            }


            const data =
                await response.json();


            console.log(
                "Vyom Assist response:",
                data
            );


            // ========================================
            // Add Command to History
            // ========================================

            addToHistory(
                command,
                data.message ||
                "Command processed."
            );


            // ========================================
            // Shutdown Confirmation
            // ========================================

            if (
                data.action ===
                "shutdown_confirmation"
            ) {

                shutdownModal.style.display =
                    "flex";

                return;

            }


            // ========================================
            // Restart Confirmation
            // ========================================

            if (
                data.action ===
                "restart_confirmation"
            ) {

                restartModal.style.display =
                    "flex";

                return;

            }


            // ========================================
            // Lock Computer
            // ========================================

            if (
                data.action ===
                "lock_computer"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // Greeting
            // ========================================

            if (
                data.action ===
                "greeting"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // Time
            // ========================================

            if (
                data.action ===
                "time"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // Date
            // ========================================

            if (
                data.action ===
                "date"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // System Information
            // ========================================

            if (
                data.action ===
                "system_info"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // System Status
            // ========================================

            if (
                data.action ===
                "system_status"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // Battery Status
            // ========================================

            if (
                data.action ===
                "battery_status"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // CPU Status
            // ========================================

            if (
                data.action ===
                "cpu_status"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // RAM Status
            // ========================================

            if (
                data.action ===
                "ram_status"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // Disk Status
            // ========================================

            if (
                data.action ===
                "disk_status"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // Internet Status
            // ========================================

            if (
                data.action ===
                "internet_status"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // Calculator
            // ========================================

            if (
                data.action ===
                "open_calculator"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // Chrome
            // ========================================

            if (
                data.action ===
                "open_chrome"
            ) {

                showResponse(
                    data.message
                );

                return;

            }


            // ========================================
            // YouTube
            // ========================================

            if (
                data.action ===
                "open_youtube"
            ) {

                window.open(
                    "https://www.youtube.com",
                    "_blank"
                );


                showResponse(
                    data.message ||
                    "Opening YouTube..."
                );


                return;

            }


            // ========================================
            // Google
            // ========================================

            if (
                data.action ===
                "open_google"
            ) {

                window.open(
                    "https://www.google.com",
                    "_blank"
                );


                showResponse(
                    data.message ||
                    "Opening Google..."
                );


                return;

            }


            // ========================================
            // Gmail
            // ========================================

            if (
                data.action ===
                "open_gmail"
            ) {

                window.open(
                    "https://mail.google.com",
                    "_blank"
                );


                showResponse(
                    data.message ||
                    "Opening Gmail..."
                );


                return;

            }


            // ========================================
            // Generic Website
            // ========================================

            if (
                data.action ===
                "open_website"
            ) {

                const website =
                    (data.website || "").trim();


                if (
                    website.startsWith(
                        "http://"
                    ) ||
                    website.startsWith(
                        "https://"
                    )
                ) {

                    window.open(
                        website,
                        "_blank"
                    );

                }

                else if (
                    website.includes(".")
                ) {

                    window.open(
                        "https://" +
                        website,
                        "_blank"
                    );

                }

                else if (
                    website !== ""
                ) {

                    window.open(
                        "https://www." +
                        website +
                        ".com",
                        "_blank"
                    );

                }


                showResponse(
                    data.message ||
                    `Opening ${website}...`
                );


                return;

            }


            // ========================================
            // Google Search
            // ========================================

            if (
                data.action ===
                "search_google"
            ) {

                const searchUrl =
                    "https://www.google.com/search?q=" +
                    encodeURIComponent(
                        data.query || ""
                    );


                window.open(
                    searchUrl,
                    "_blank"
                );


                showResponse(
                    data.message ||
                    `Searching Google for "${data.query}"...`
                );


                return;

            }


            // ========================================
            // Default Response
            // ========================================

            showResponse(
                data.message ||
                "Command processed."
            );

        }


        catch (error) {

            console.error(
                "Vyom Assist frontend error:",
                error
            );


            showResponse(
                "Could not connect to Vyom Assist backend."
            );

        }


        finally {

            sendCommandButton.disabled =
                false;

        }

    }
);


// ========================================
// Enter Key Support
// ========================================

commandInput.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter" &&
            !sendCommandButton.disabled
        ) {

            sendCommandButton.click();

        }

    }
);


// ========================================
// Voice Button
// ========================================

voiceButton.addEventListener(
    "click",
    function () {

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;


        // ========================================
        // Browser Support
        // ========================================

        if (!SpeechRecognition) {

            showResponse(
                "Speech recognition is not supported in this browser."
            );

            return;

        }


        const recognition =
            new SpeechRecognition();


        recognition.lang =
            "en-US";


        recognition.continuous =
            false;


        recognition.interimResults =
            false;


        // ========================================
        // Listening State
        // ========================================

        voiceButton.textContent =
            "🎙️ Listening...";


        voiceButton.disabled =
            true;


        showResponse(
            "Listening for your command..."
        );


        try {

            recognition.start();

        }

        catch (error) {

            console.error(
                "Speech recognition start error:",
                error
            );

        }


        // ========================================
        // Voice Result
        // ========================================

        recognition.onresult =
            function (event) {

                const spokenCommand =
                    event.results[0][0]
                        .transcript;


                commandInput.value =
                    spokenCommand;


                // Automatically send command

                sendCommandButton.click();

            };


        // ========================================
        // Voice Error
        // ========================================

        recognition.onerror =
            function (event) {

                if (
                    event.error ===
                    "no-speech"
                ) {

                    showResponse(
                        "No speech detected. Please try again."
                    );

                    return;

                }


                if (
                    event.error ===
                    "not-allowed"
                ) {

                    showResponse(
                        "Microphone permission is required."
                    );

                    return;

                }


                showResponse(
                    "Voice recognition error. Please try again."
                );

            };


        // ========================================
        // Voice End
        // ========================================

        recognition.onend =
            function () {

                voiceButton.textContent =
                    "🎤 Speak Command";


                voiceButton.disabled =
                    false;

            };

    }
);


// ========================================
// Shutdown - Yes
// ========================================

shutdownYesButton.addEventListener(
    "click",
    async function () {

        const finalConfirm =
            confirm(
                "Final confirmation: Do you really want to shut down this computer?"
            );


        if (!finalConfirm) {

            shutdownModal.style.display =
                "none";


            showResponse(
                "Shutdown cancelled."
            );


            return;

        }


        shutdownModal.style.display =
            "none";


        showProcessing();


        try {

            const response =
                await fetch(
                    "http://localhost:5000/shutdown",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        }
                    }
                );


            const data =
                await response.json();


            showResponse(
                data.message ||
                "Shutdown command sent."
            );

        }


        catch (error) {

            console.error(
                "Shutdown error:",
                error
            );


            showResponse(
                "Could not connect to Vyom Assist backend."
            );

        }

    }
);


// ========================================
// Shutdown - No
// ========================================

shutdownNoButton.addEventListener(
    "click",
    function () {

        shutdownModal.style.display =
            "none";


        showResponse(
            "Shutdown cancelled."
        );

    }
);


// ========================================
// Restart - Yes
// ========================================

restartYesButton.addEventListener(
    "click",
    async function () {

        const finalConfirm =
            confirm(
                "Final confirmation: Do you really want to restart this computer?"
            );


        if (!finalConfirm) {

            restartModal.style.display =
                "none";


            showResponse(
                "Restart cancelled."
            );


            return;

        }


        restartModal.style.display =
            "none";


        showProcessing();


        try {

            const response =
                await fetch(
                    "http://localhost:5000/restart",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        }
                    }
                );


            const data =
                await response.json();


            console.log(
                "Restart response:",
                data
            );


            showResponse(
                data.message ||
                "Restart command sent."
            );

        }


        catch (error) {

            console.error(
                "Restart error:",
                error
            );


            showResponse(
                "Could not connect to Vyom Assist backend."
            );

        }

    }
);


// ========================================
// Restart - No
// ========================================

restartNoButton.addEventListener(
    "click",
    function () {

        restartModal.style.display =
            "none";


        showResponse(
            "Restart cancelled."
        );

    }
);