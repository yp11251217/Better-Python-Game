import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Universal Hole.io", layout="wide")

st.title("🕳️ Universal Hole.io (PC + Mobile)")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">

<style>
    body {
        margin: 0;
        overflow: hidden;
        background: #111;
        touch-action: none;
    }

    canvas {
        display: block;
        background: radial-gradient(circle, #222, #000);
    }

    #hud {
        position: absolute;
        top: 10px;
        left: 10px;
        color: white;
        font-family: Arial;
        font-size: 16px;
        z-index: 10;
    }

    /* Mobile joystick */
    #joystickArea {
        position: absolute;
        bottom: 25px;
        left: 25px;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        display: none; /* hidden on PC by default */
    }

    #stick {
        position: absolute;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        top: 35px;
        left: 35px;
    }
</style>
</head>

<body>
<div id="hud">Size: <span id="size">10</span></div>

<div id="joystickArea">
    <div id="stick"></div>
</div>

<canvas id="game"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

/* ---------------- DEVICE DETECTION ---------------- */
const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

if (isMobile) {
    document.getElementById("joystickArea").style.display = "block";
}

/* ---------------- PLAYER ---------------- */
let player = {
    x: canvas.width/2,
    y: canvas.height/2,
    r: 12
};

/* ---------------- FOOD ---------------- */
let food = [];
for (let i = 0; i < 80; i++) {
    food.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 8 + 2
    });
}

/* ---------------- KEYBOARD CONTROLS (PC) ---------------- */
let keys = {};

document.addEventListener("keydown", e => keys[e.key.toLowerCase()] = true);
document.addEventListener("keyup", e => keys[e.key.toLowerCase()] = false);

/* ---------------- JOYSTICK (MOBILE) ---------------- */
let joystick = { dx: 0, dy: 0 };

const area = document.getElementById("joystickArea");
const stick = document.getElementById("stick");

function moveStick(x, y) {
    stick.style.left = x + "px";
    stick.style.top = y + "px";
}

if (isMobile) {
    area.addEventListener("touchstart", e => {});
    
    area.addEventListener("touchmove", e => {
        let t = e.touches[0];
        let rect = area.getBoundingClientRect();

        let dx = t.clientX - (rect.left + rect.width/2);
        let dy = t.clientY - (rect.top + rect.height/2);

        let max = 40;
        let dist = Math.min(max, Math.sqrt(dx*dx + dy*dy));
        let angle = Math.atan2(dy, dx);

        joystick.dx = Math.cos(angle) * dist / max;
        joystick.dy = Math.sin(angle) * dist / max;

        moveStick(35 + joystick.dx*40, 35 + joystick.dy*40);
    });

    area.addEventListener("touchend", () => {
        joystick.dx = 0;
        joystick.dy = 0;
        moveStick(35, 35);
    });
}

/* ---------------- GAME LOOP ---------------- */

function update() {
    let speed = 5;

    // PC movement
    if (keys["w"] || keys["arrowup"]) player.y -= speed;
    if (keys["s"] || keys["arrowdown"]) player.y += speed;
    if (keys["a"] || keys["arrowleft"]) player.x -= speed;
    if (keys["d"] || keys["arrowright"]) player.x += speed;

    // Mobile movement
    player.x += joystick.dx * speed;
    player.y += joystick.dy * speed;

    // bounds
    player.x = Math.max(player.r, Math.min(canvas.width-player.r, player.x));
    player.y = Math.max(player.r, Math.min(canvas.height-player.r, player.y));

    // eating logic
    for (let i = 0; i < food.length; i++) {
        let f = food[i];
        let dx = player.x - f.x;
        let dy = player.y - f.y;
        let dist = Math.sqrt(dx*dx + dy*dy);

        if (dist < player.r + f.r) {
            if (player.r >= f.r) {
                player.r += 0.2;
                food[i] = {
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    r: Math.random() * 8 + 2
                };
            } else {
                player.r = 12;
            }
        }
    }

    document.getElementById("size").innerText = player.r.toFixed(1);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // food
    for (let f of food) {
        ctx.beginPath();
        ctx.fillStyle = "#4ade80";
        ctx.arc(f.x, f.y, f.r, 0, Math.PI*2);
        ctx.fill();
    }

    // player
    ctx.beginPath();
    ctx.fillStyle = "black";
    ctx.arc(player.x, player.y, player.r, 0, Math.PI*2);
    ctx.fill();

    ctx.strokeStyle = "white";
    ctx.stroke();
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

loop();
</script>

</body>
</html>
"""

components.html(html_code, height=800, scrolling=False)
