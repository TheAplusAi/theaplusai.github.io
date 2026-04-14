const API_BASE = "https://theaplusai-github-io.onrender.com";

// ------------------ CHAT ------------------
async function sendMessage() {
    const input = document.getElementById("msg-input");
    const message = input.value.trim();

    if (message === "") return;

    addMessage(message, "user");
    input.value = "";

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await res.json();

        if (data.reply) {
            addMessage(data.reply, "ai");
        } else if (data.error) {
            addMessage("⚠️ " + data.error, "ai");
        } else {
            addMessage("No response from AI", "ai");
        }

    } catch (err) {
        console.error(err);
        addMessage("⚠️ Error connecting to AI", "ai");
    }
}

// ------------------ UI MESSAGE ------------------
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

// ------------------ ENTER KEY ------------------
document.getElementById("msg-input").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// ------------------ LOGIN MODAL ------------------
function openAuthModal() {
    document.getElementById("authModal").style.display = "flex";
}

function closeAuthModal() {
    document.getElementById("authModal").style.display = "none";
}

// ------------------ SIGNUP ------------------
async function signup() {
    const email = document.getElementById("email").value;
    const pass = document.getElementById("password").value;

    if (!email || !pass) {
        alert("Enter details");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/signup`, {
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

        // 🔥 LOGIN STATE
        localStorage.setItem("user", email);

        document.getElementById("loginBtn").style.display = "none";
        document.getElementById("profileIcon").style.display = "block";

        closeAuthModal();

    } catch (err) {
        console.error(err);
        alert("Signup error");
    }
}

// ------------------ LOGOUT ------------------
function logout() {
    localStorage.removeItem("user");

    document.getElementById("loginBtn").style.display = "inline-block";
    document.getElementById("profileIcon").style.display = "none";
}

// ------------------ PERSIST LOGIN ------------------
window.onload = function () {
    const user = localStorage.getItem("user");

    if (user) {
        document.getElementById("loginBtn").style.display = "none";
        document.getElementById("profileIcon").style.display = "block";
    }
};

// ------------------ TOP ALERT ------------------
function showComingSoon() {
    const el = document.getElementById("topAlert");

    if (!el) return;

    el.classList.add("show");

    setTimeout(() => {
        el.classList.remove("show");
    }, 2500);
}
