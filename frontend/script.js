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


// ========================================
// Response Status Elements
// ========================================

const responseStatusIndicator =
    document.getElementById("responseStatusIndicator");

const responseStatusText =
    document.getElementById("responseStatusText");


// ========================================
// Shutdown
// ========================================

const shutdownModal =
    document.getElementById("shutdownModal");

const shutdownYesButton =
    document.getElementById("shutdownYesButton");

const shutdownNoButton =
    document.getElementById("shutdownNoButton");


// ========================================
// Restart
// ========================================

const restartModal =
    document.getElementById("restartModal");

const restartYesButton =
    document.getElementById("restartYesButton");

const restartNoButton =
    document.getElementById("restartNoButton");


// ========================================
// History
// ========================================

const historyList =
    document.getElementById("historyList");

const clearHistoryButton =
    document.getElementById("clearHistoryButton");


// ========================================
// Local Storage Key
// ========================================

const HISTORY_STORAGE_KEY =
    "vyomAssistCommandHistory";


// ========================================
// Python Emotion API
// ========================================

const PYTHON_ASSISTANT_URL =
    "http://127.0.0.1:5001";


// ========================================
// Emotion Variables
// ========================================
let currentEmotion = "Neutral";
let emotionCard = null;

let emotionNameElement = null;

let emotionConfidenceElement = null;

let emotionStatusElement = null;

let emotionInterval = null;


// ========================================
// Create Emotion Card
// ========================================

function createEmotionCard() {

    // Prevent duplicate card
    if (emotionCard) {
        return emotionCard;
    }


    // ========================================
    // Main Card
    // ========================================

    emotionCard =
        document.createElement("div");


    emotionCard.id =
        "emotionCard";


    emotionCard.style.marginTop =
        "15px";

    emotionCard.style.padding =
        "15px";

    emotionCard.style.border =
        "1px solid rgba(255,255,255,0.15)";

    emotionCard.style.borderRadius =
        "12px";

    emotionCard.style.background =
        "rgba(255,255,255,0.05)";

    emotionCard.style.fontFamily =
        "Arial, sans-serif";


    // ========================================
    // Title
    // ========================================

    const title =
        document.createElement("div");


    title.textContent =
        "😊 Current Emotion";


    title.style.fontSize =
        "18px";

    title.style.fontWeight =
        "bold";

    title.style.marginBottom =
        "8px";


    // ========================================
    // Emotion Name
    // ========================================

    emotionNameElement =
        document.createElement("div");


    emotionNameElement.id =
        "emotionName";


    emotionNameElement.textContent =
        "Waiting...";


    emotionNameElement.style.fontSize =
        "20px";

    emotionNameElement.style.fontWeight =
        "bold";


    // ========================================
    // Confidence
    // ========================================

    emotionConfidenceElement =
        document.createElement("div");


    emotionConfidenceElement.id =
        "emotionConfidence";


    emotionConfidenceElement.textContent =
        "Confidence: --";


    emotionConfidenceElement.style.marginTop =
        "5px";

    emotionConfidenceElement.style.opacity =
        "0.8";


    // ========================================
    // Status
    // ========================================

    emotionStatusElement =
        document.createElement("div");


    emotionStatusElement.id =
        "emotionStatus";


    emotionStatusElement.textContent =
        "Emotion detection ready.";


    emotionStatusElement.style.marginTop =
        "5px";

    emotionStatusElement.style.fontSize =
        "13px";

    emotionStatusElement.style.opacity =
        "0.7";


    // ========================================
    // Add Elements To Card
    // ========================================

    emotionCard.appendChild(
        title
    );


    emotionCard.appendChild(
        emotionNameElement
    );


    emotionCard.appendChild(
        emotionConfidenceElement
    );


    emotionCard.appendChild(
        emotionStatusElement
    );


    // ========================================
    // Insert Card
    // ========================================

    if (
        responseBox &&
        responseBox.parentNode
    ) {

        responseBox.parentNode.insertBefore(
            emotionCard,
            responseBox.nextSibling
        );

    }

    else {

        document.body.appendChild(
            emotionCard
        );

    }


    return emotionCard;

}


// ========================================
// Emotion Emoji
// ========================================

function getEmotionEmoji(emotion) {

    const emotionMap = {

        "Angry": "😠",

        "Disgust": "🤢",

        "Fearful": "😨",

        "Happy": "😊",

        "Neutral": "😐",

        "Sad": "😢",

        "Surprised": "😲"

    };


    return (
        emotionMap[emotion] ||
        "🙂"
    );

}


// ========================================
// Update Emotion Card
// ========================================

function updateEmotionCard(
    emotion,
    confidence,
    statusMessage
) {

    currentEmotion = emotion;
    createEmotionCard();


    if (emotionNameElement) {

        emotionNameElement.textContent =
            `${getEmotionEmoji(emotion)} ${emotion} `;

    }


    if (emotionConfidenceElement) {

        emotionConfidenceElement.textContent =
            `Confidence: ${confidence}% `;

    }


    if (emotionStatusElement) {

        emotionStatusElement.textContent =
            statusMessage ||
            "Emotion detected successfully.";

    }

}


// ========================================
// Emotion Detection
// ========================================

async function detectEmotion() {

    createEmotionCard();


    // ========================================
    // Detection State
    // ========================================

    if (emotionNameElement) {

        emotionNameElement.textContent =
            "🔍 Detecting...";

    }


    if (emotionConfidenceElement) {

        emotionConfidenceElement.textContent =
            "Confidence: --";

    }


    if (emotionStatusElement) {

        emotionStatusElement.textContent =
            "Connecting to emotion detection...";

    }


    try {

        const response =
            await fetch(
                `${PYTHON_ASSISTANT_URL}/emotion`
            );


        if (!response.ok) {

            throw new Error(
                `Emotion API returned ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "Vyom Assist emotion response:",
            data
        );


        // ========================================
        // Successful Detection
        // ========================================

        if (
            data.success &&
            data.face_detected &&
            data.emotion
        ) {

            updateEmotionCard(
                data.emotion,
                data.confidence_percent ?? "N/A",
                data.message ||
                "Emotion detected successfully."
            );


            return data;

        }


        // ========================================
        // Face Not Detected
        // ========================================

        if (
            data.success &&
            !data.face_detected
        ) {

            if (emotionNameElement) {

                emotionNameElement.textContent =
                    "👤 Face not detected";

            }


            if (emotionConfidenceElement) {

                emotionConfidenceElement.textContent =
                    "Confidence: --";

            }


            if (emotionStatusElement) {

                emotionStatusElement.textContent =
                    "Please make sure your face is visible to the camera.";

            }


            return data;

        }


        // ========================================
        // API Error
        // ========================================

        throw new Error(
            data.message ||
            "Emotion detection failed."
        );

    }


    catch (error) {

        console.error(
            "Emotion detection error:",
            error
        );


        if (emotionNameElement) {

            emotionNameElement.textContent =
                "⚠️ Emotion unavailable";

        }


        if (emotionConfidenceElement) {

            emotionConfidenceElement.textContent =
                "Confidence: --";

        }


        if (emotionStatusElement) {

            emotionStatusElement.textContent =
                "Could not connect to Python emotion service.";

        }


        return null;

    }

}


// ========================================
// Start Continuous Emotion Detection
// ========================================

function startContinuousEmotionDetection() {

    // Prevent duplicate intervals
    stopContinuousEmotionDetection();


    // Immediate detection
    detectEmotion();


    // Detect every 3 seconds
    emotionInterval =
        setInterval(
            function () {

                detectEmotion();

            },
            3000
        );

}


// ========================================
// Stop Continuous Emotion Detection
// ========================================

function stopContinuousEmotionDetection() {

    if (emotionInterval !== null) {

        clearInterval(
            emotionInterval
        );

        emotionInterval = null;

    }

}


// ========================================
// Voice Response - Text To Speech
// ========================================

function speakResponse(message) {

    if (!message) {
        return;
    }


    if (
        !("speechSynthesis" in window) ||
        !("SpeechSynthesisUtterance" in window)
    ) {

        return;

    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            message
        );


    speech.lang =
        "en-US";

    speech.rate =
        1;

    speech.pitch =
        1;

    speech.volume =
        1;


    window.speechSynthesis.speak(
        speech
    );

}


// ========================================
// Scroll To Response
// ========================================

function scrollToResponse() {

    // No automatic scrolling required.

}


// ========================================
// Response Status
// ========================================

function setResponseStatus(status) {

    if (!responseBox) {
        return;
    }


    responseBox.classList.remove(
        "status-ready",
        "status-processing",
        "status-listening",
        "status-error"
    );


    // ========================================
    // Ready
    // ========================================

    if (status === "ready") {

        responseBox.classList.add(
            "status-ready"
        );


        if (responseStatusIndicator) {

            responseStatusIndicator.textContent =
                "🟢";

        }


        if (responseStatusText) {

            responseStatusText.textContent =
                "Ready";

        }


        return;

    }


    // ========================================
    // Processing
    // ========================================

    if (status === "processing") {

        responseBox.classList.add(
            "status-processing"
        );


        if (responseStatusIndicator) {

            responseStatusIndicator.textContent =
                "🟡";

        }


        if (responseStatusText) {

            responseStatusText.textContent =
                "Processing";

        }


        return;

    }


    // ========================================
    // Listening
    // ========================================

    if (status === "listening") {

        responseBox.classList.add(
            "status-listening"
        );


        if (responseStatusIndicator) {

            responseStatusIndicator.textContent =
                "🔵";

        }


        if (responseStatusText) {

            responseStatusText.textContent =
                "Listening";

        }


        return;

    }


    // ========================================
    // Error
    // ========================================

    if (status === "error") {

        responseBox.classList.add(
            "status-error"
        );


        if (responseStatusIndicator) {

            responseStatusIndicator.textContent =
                "🔴";

        }


        if (responseStatusText) {

            responseStatusText.textContent =
                "Error";

        }


        return;

    }


    // ========================================
    // Default
    // ========================================

    responseBox.classList.add(
        "status-ready"
    );


    if (responseStatusIndicator) {

        responseStatusIndicator.textContent =
            "🟢";

    }


    if (responseStatusText) {

        responseStatusText.textContent =
            "Ready";

    }

}


// ========================================
// Show Assistant Response
// ========================================

function showResponse(
    message,
    status = "ready",
    shouldSpeak = true
) {

    const finalMessage =
        message ||
        "Command processed.";


    if (responseMessage) {

        responseMessage.textContent =
            finalMessage;

    }


    setResponseStatus(
        status
    );


    if (shouldSpeak) {

        speakResponse(
            finalMessage
        );

    }


    scrollToResponse();

}


// ========================================
// Processing Indicator
// ========================================

function showProcessing() {

    if (responseMessage) {

        responseMessage.textContent =
            "⏳ Vyom Assist is processing...";

    }


    setResponseStatus(
        "processing"
    );


    scrollToResponse();

}


// ========================================
// Command History
// ========================================

function addToHistory(
    command,
    response
) {

    if (!historyList) {
        return;
    }


    const emptyMessage =
        historyList.querySelector(
            ".empty-history"
        );


    if (emptyMessage) {

        emptyMessage.remove();

    }


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


    historyItem.appendChild(
        commandLine
    );


    historyItem.appendChild(
        responseLine
    );


    historyList.prepend(
        historyItem
    );

}


// ========================================
// Save History To Local Storage
// ========================================

function saveHistory(
    command,
    response
) {

    let history = [];


    try {

        const savedHistory =
            localStorage.getItem(
                HISTORY_STORAGE_KEY
            );


        if (savedHistory) {

            history =
                JSON.parse(
                    savedHistory
                );

        }

    }

    catch (error) {

        console.error(
            "Could not read saved history:",
            error
        );

        history = [];

    }


    if (!Array.isArray(history)) {

        history = [];

    }


    history.unshift({
        command: command,
        response: response
    });


    try {

        localStorage.setItem(
            HISTORY_STORAGE_KEY,
            JSON.stringify(history)
        );

    }

    catch (error) {

        console.error(
            "Could not save command history:",
            error
        );

    }

}


// ========================================
// Load History From Local Storage
// ========================================

function loadHistory() {

    if (!historyList) {
        return;
    }


    let history = [];


    try {

        const savedHistory =
            localStorage.getItem(
                HISTORY_STORAGE_KEY
            );


        if (savedHistory) {

            history =
                JSON.parse(
                    savedHistory
                );

        }

    }

    catch (error) {

        console.error(
            "Could not load saved history:",
            error
        );

        history = [];

    }


    if (!Array.isArray(history)) {

        history = [];

    }


    if (history.length === 0) {

        return;

    }


    const emptyMessage =
        historyList.querySelector(
            ".empty-history"
        );


    if (emptyMessage) {

        emptyMessage.remove();

    }


    history.forEach(
        function (item) {

            if (
                !item ||
                typeof item.command !== "string" ||
                typeof item.response !== "string"
            ) {

                return;

            }


            const historyItem =
                document.createElement("div");


            historyItem.className =
                "history-item";


            // ========================================
            // User
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
                item.command;


            commandLine.appendChild(
                commandLabel
            );


            commandLine.appendChild(
                commandText
            );


            // ========================================
            // Assistant
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
                item.response;


            responseLine.appendChild(
                responseLabel
            );


            responseLine.appendChild(
                responseText
            );


            historyItem.appendChild(
                commandLine
            );


            historyItem.appendChild(
                responseLine
            );


            historyList.appendChild(
                historyItem
            );

        }
    );

}


// ========================================
// Clear Command History
// ========================================

if (clearHistoryButton) {

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


            localStorage.removeItem(
                HISTORY_STORAGE_KEY
            );


            showResponse(
                "Command history cleared."
            );

        }
    );

}


// ========================================
// Load Saved History
// ========================================

loadHistory();


// ========================================
// Start Assistant
// ========================================

if (startButton) {

    startButton.addEventListener(
        "click",
        async function () {

            const startupMessage =
                "🟢 Vyom Assist is ready!\n\n" +
                "Voice commands are available.\n" +
                "You can ask me to open applications, websites, search Google, " +
                "check system status, battery, CPU, RAM, disk, and more.";


            showResponse(
                startupMessage
            );


            // ========================================
            // Start Continuous Emotion Detection
            // ========================================

            startContinuousEmotionDetection();

        }
    );

}


// ========================================
// Send Command
// ========================================

if (sendCommandButton) {

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
                                command: command,
                                emotion: currentEmotion
                            })
                        }
                    );


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
                // History
                // ========================================

                const historyResponse =
                    data.message ||
                    "Command processed.";


                addToHistory(
                    command,
                    historyResponse
                );


                saveHistory(
                    command,
                    historyResponse
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


                    showResponse(
                        data.message ||
                        "Shutdown confirmation required.",
                        "ready",
                        false
                    );


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


                    showResponse(
                        data.message ||
                        "Restart confirmation required.",
                        "ready",
                        false
                    );


                    return;

                }


                // ========================================
                // Direct Actions
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


                if (
                    data.action ===
                    "greeting"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


                if (
                    data.action ===
                    "time"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


                if (
                    data.action ===
                    "date"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


                if (
                    data.action ===
                    "system_info"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


                if (
                    data.action ===
                    "system_status"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


                if (
                    data.action ===
                    "battery_status"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


                if (
                    data.action ===
                    "cpu_status"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


                if (
                    data.action ===
                    "ram_status"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


                if (
                    data.action ===
                    "disk_status"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


                if (
                    data.action ===
                    "internet_status"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


                if (
                    data.action ===
                    "open_calculator"
                ) {

                    showResponse(
                        data.message
                    );

                    return;

                }


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
                // Default
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
                    "Could not connect to Vyom Assist backend.",
                    "error"
                );

            }


            finally {

                sendCommandButton.disabled =
                    false;

            }

        }
    );

}


// ========================================
// Enter Key Support
// ========================================

if (commandInput) {

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

}


// ========================================
// Voice Button
// ========================================

if (voiceButton) {

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
                    "Speech recognition is not supported in this browser.",
                    "error"
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


            if (responseMessage) {

                responseMessage.textContent =
                    "🎙️ Listening for your command...";

            }


            setResponseStatus(
                "listening"
            );


            scrollToResponse();


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
                            .transcript
                            .trim();


                    commandInput.value =
                        spokenCommand;


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
                            "No speech detected. Please try again.",
                            "error"
                        );


                        return;

                    }


                    if (
                        event.error ===
                        "not-allowed"
                    ) {

                        showResponse(
                            "Microphone permission is required.",
                            "error"
                        );


                        return;

                    }


                    showResponse(
                        "Voice recognition error. Please try again.",
                        "error"
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

}


// ========================================
// Shutdown - Yes
// ========================================

if (shutdownYesButton) {

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
                    "Could not connect to Vyom Assist backend.",
                    "error"
                );

            }

        }
    );

}


// ========================================
// Shutdown - No
// ========================================

if (shutdownNoButton) {

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

}


// ========================================
// Restart - Yes
// ========================================

if (restartYesButton) {

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
                    "Could not connect to Vyom Assist backend.",
                    "error"
                );

            }

        }
    );

}


// ========================================
// Restart - No
// ========================================

if (restartNoButton) {

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

}

