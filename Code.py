import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mobile Hole.io", layout="wide")

st.title("🕳️ Mobile Hole.io")

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
        touch-action: none; /* IMPORTANT for mobile drag */
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
        font-size: 16px;
        z-index: 10;
        font-family: Arial;
    }

    #joystickArea {
        position: absolute;
        bottom: 30px;
        left: 30px;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        touch-action: none;
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

let player = {
    x: canvas.width/2,
    y: canvas.height/2,
    r: 12,
    vx: 0,
    vy: 0
};

let food = [];
for (let i = 0; i < 70; i++) {
    food.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 8 + 2
    });
}

/* ---------------- TOUCH JOYSTICK ---------------- */
let joystick = {
    active: false,
    dx: 0,
    dy: 0
};

const area = document.getElementById("joystickArea");
const stick = document.getElementById("stick");

function setStickPosition(x, y) {
    stick.style.left = x + "px";
    stick.style.top = y + "px";
}

area.addEventListener("touchstart", e => {
    joystick.active = true;
});

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

    setStickPosition(
        35 + joystick.dx * 40,
        35 + joystick.dy * 40
    );
});

area.addEventListener("touchend", () => {
    joystick.dx = 0;
    joystick.dy = 0;
    setStickPosition(35, 35);
});

/* ---------------- GAME LOGIC ---------------- */

function update() {
    player.x += joystick.dx * 5;
    player.y += joystick.dy * 5;

    player.x = Math.max(player.r, Math.min(canvas.width-player.r, player.x));
    player.y = Math.max(player.r, Math.min(canvas.height-player.r, player.y));

    for (let i = 0; i < food.length; i++) {
        let f = food[i];
        let dx = player.x - f.x;
        let dy = player.y - f.y;
        let dist = Math.sqrt(dx*dx + dy*dy);

        if (dist < player.r + f.r) {
            if (player.r >= f.r) {
                player.r += 0.25;
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

    for (let f of food) {
        ctx.beginPath();
        ctx.fillStyle = "#4ade80";
        ctx.arc(f.x, f.y, f.r, 0, Math.PI*2);
        ctx.fill();
    }

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
