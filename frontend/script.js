const startButton = document.getElementById("startButton");
const commandInput = document.getElementById("commandInput");
const sendCommandButton = document.getElementById("sendCommandButton");

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
        } else {
            alert(data.message);
        }

    } catch (error) {
        alert("Could not connect to Vyom Assist backend.");
        console.error(error);
    }
});