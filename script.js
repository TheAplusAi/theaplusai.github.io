// ------------------ SEND MESSAGE ------------------
async function sendMessage() {
    const input = document.getElementById("msg-input");
    const message = input.value.trim();

    if (message === "") return;

    addMessage(message, "user");
    input.value = "";

    try {
        const res = await fetch("https://theaplusai-github-io.onrender.com/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await res.json();

        // ✅ FIXED ERROR HANDLING
        if (data.reply) {
            addMessage(data.reply, "ai");
        } else if (data.error) {
            console.error("BACKEND ERROR:", data.error);
            addMessage("⚠️ " + data.error, "ai");
        } else {
            addMessage("No response from AI", "ai");
        }

    } catch (err) {
        console.error("CHAT ERROR:", err);
        addMessage("⚠️ Error connecting to AI", "ai");
    }
}
// ------------------ ADD MESSAGE UI ------------------
function addMessage(text, sender) {
    const chat = document.getElementById("chat-messages");
    const msg = document.createElement("div");

    msg.innerText = text;
    msg.style.padding = "10px";
    msg.style.margin = "8px 0";
    msg.style.borderRadius = "10px";
    msg.style.maxWidth = "70%";

    if (sender === "user") {
        msg.style.background = "#2563eb";
        msg.style.color = "white";
        msg.style.marginLeft = "auto";
        msg.style.textAlign = "right";
    } else {
        msg.style.background = "#333";
        msg.style.color = "white";
    }

    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}


// ------------------ ENTER KEY SEND ------------------
document.getElementById("msg-input").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});


// ------------------ MODAL ------------------
function openAuthModal() {
    document.getElementById("authModal").style.display = "flex";
}

function closeAuthModal() {
    document.getElementById("authModal").style.display = "none";
}


// ------------------ SIGNUP ONLY (LOGIN REMOVED FOR NOW) ------------------
async function signup() {
    const email = document.getElementById("email").value;
    const pass = document.getElementById("password").value;

    if (!email || !pass) {
        alert("Enter details bro");
        return;
    }

    try {
        const res = await fetch("https://theaplusai-github-io.onrender.com/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: email,
                password: pass
            })
        });

        const data = await res.json();
        alert(data.message);

    } catch (err) {
        console.error("SIGNUP ERROR:", err);
        alert("Signup error");
    }
}

function showComingSoon() {
    const el = document.getElementById("topAlert");

    if (!el) return;

    el.classList.add("show");

    setTimeout(() => {
        el.classList.remove("show");
    }, 2500);
}
