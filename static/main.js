const chatMessages = document.getElementById("chat-messages");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

// Add message to chat
function addMessage(msg, sender){
    const div = document.createElement("div");
    div.classList.add("message");
    div.classList.add(sender === "user" ? "user-msg" : "bot-msg");
    div.innerText = msg;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send button click
sendBtn.addEventListener("click", async () => {
    const message = chatInput.value.trim();
    if(message === "") return;
    addMessage(message, "user");
    chatInput.value = "";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message})
        });
        const data = await res.json();
        addMessage(data.reply, "bot");
    } catch (err) {
        addMessage("Sorry, AI is unavailable.", "bot");
    }
});

// Prevent Enter key from sending
chatInput.addEventListener("keydown", (e) => {
    if(e.key === "Enter") e.preventDefault();
});
