// // static/main.js
// async function postJSON(url, body){
//   const res = await fetch(url, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify(body)
//   });
//   return res.json();
// }

// function appendMessage(text, cls="bot"){
//   const cont = document.getElementById("messages");
//   const el = document.createElement("div");
//   el.className = "message " + (cls === "me" ? "me" : "bot");
//   el.innerHTML = `<div>${text}</div>`;
//   cont.appendChild(el);
//   cont.scrollTop = cont.scrollHeight;
// }

// document.getElementById("send").onclick = async () => {
//   const input = document.getElementById("msg");
//   const text = input.value.trim();
//   if(!text) return;
//   appendMessage(text, "me");
//   input.value = "";
//   // show typing indicator
//   appendMessage("Typing...", "bot");
//   try {
//     const resp = await postJSON("/chat", { message: text });
//     // remove last typing
//     const msgs = document.getElementById("messages");
//     msgs.removeChild(msgs.lastChild);
//     if(resp.error){
//       appendMessage("Error: " + resp.error, "bot");
//     } else {
//       appendMessage(resp.reply, "bot");
//     }
//   } catch(err){
//     // remove last typing
//     const msgs = document.getElementById("messages");
//     msgs.removeChild(msgs.lastChild);
//     appendMessage("Network error", "bot");
//     console.error(err);
//   }
// };

// document.getElementById("leadBtn").onclick = async () => {
//   const name = prompt("Your name?");
//   const phone = prompt("Phone number?");
//   if(!name || !phone){ alert("Name & phone are required"); return; }
//   const email = prompt("Email (optional)");
//   const message = prompt("A short message (optional)");
//   appendMessage(`Lead submitted: ${name} — ${phone}`, "me");
//   try {
//     const r = await postJSON("/save_lead", { name, phone, email, message });
//     if(r.error) appendMessage("Lead error: " + r.error, "bot");
//     else appendMessage("Thanks — we'll call you soon!", "bot");
//   } catch(e){
//     appendMessage("Lead save failed", "bot");
//   }
// };


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
