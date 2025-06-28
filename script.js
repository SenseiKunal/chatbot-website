// Add message to chat window and sidebar history
function addMessage(role, text) {
  const chatBox = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = role;
  div.innerHTML = `<strong>${role === "user" ? "You" : "Bot"}:</strong> ${text}`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;

  if (role === "user") {
    const historyList = document.getElementById("history-list");
    const li = document.createElement("li");
    li.textContent = text;
    historyList.appendChild(li);
  }
}

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    addMessage("bot", data.reply);
  } catch (err) {
    addMessage("bot", "Sorry, error occurred!");
  }
}

// Send on Enter key press
document.getElementById("user-input").addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
});
