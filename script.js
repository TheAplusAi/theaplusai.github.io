// Send message to backend
async function sendMessage() {
    const input = document.getElementById("msg-input");
    const message = input.value.trim();

    if (message === "") return;

    // Show user message
    addMessage(message, "user");
    input.value = "";

    try {
        const res = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await res.json();

        // Show AI reply
        addMessage(data.reply || "No response from AI", "ai");

    } catch (err) {
        console.error(err);
        addMessage("⚠️ Error connecting to AI", "ai");
    }
}


// Add message to chat UI
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


document.getElementById("msg-input").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault(); // stop new line
        sendMessage();
    }
});

function openAuthModal() {
    document.getElementById("authModal").style.display = "flex";
}

function closeAuthModal() {
    document.getElementById("authModal").style.display = "none";
}

async function login() {
    console.log("LOGIN CLICKED"); // debug

    const email = document.getElementById("email")?.value || document.getElementById("username")?.value;
    const pass = document.getElementById("password").value;

    if (!email || !pass) {
        alert("Enter details bro");
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:5000/login", {
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

        if (data.success) {
            alert("Login successful 😎");

            document.getElementById("loginBtn").style.display = "none";
            document.getElementById("profileIcon").style.display = "block";

            localStorage.setItem("loggedIn", "true");

            closeAuthModal();
        } else {
            alert(data.message);
        }

    } catch (err) {
        console.error(err);
        alert("Server error");
    }
}

// LOGIN
async function login() {
    console.log("LOGIN CLICKED");

    const email = document.getElementById("email").value;
    const pass = document.getElementById("password").value;

    if (!email || !pass) {
        alert("Enter details bro");
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:5000/login", {
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

        if (data.success) {
            alert("Login successful 😎");

            document.getElementById("loginBtn").style.display = "none";
            document.getElementById("profileIcon").style.display = "block";

            localStorage.setItem("loggedIn", "true");

            closeAuthModal();
        } else {
            alert(data.message);
        }

    } catch (err) {
        console.error(err);
        alert("Server error");
    }
}


// SIGNUP
async function signup() {
    const email = document.getElementById("email").value;
    const pass = document.getElementById("password").value;

    if (!email || !pass) {
        alert("Enter details bro");
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:5000/signup", {
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
        console.error(err);
        alert("Signup error");
    }
}