import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mini Hole.io", layout="wide")

st.title("🕳️ Mini Hole.io (Streamlit + HTML Game)")
st.write("Move with WASD or Arrow Keys. Eat smaller dots to grow!")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        overflow: hidden;
        background: #111;
        font-family: Arial;
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
        font-size: 18px;
        z-index: 10;
    }
</style>
</head>
<body>
<div id="hud">Size: <span id="size">10</span></div>
<canvas id="game"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let player = {
    x: canvas.width/2,
    y: canvas.height/2,
    r: 10,
    speed: 4
};

let keys = {};

let food = [];
for (let i = 0; i < 60; i++) {
    food.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 8 + 2
    });
}

document.addEventListener("keydown", e => keys[e.key.toLowerCase()] = true);
document.addEventListener("keyup", e => keys[e.key.toLowerCase()] = false);

function update() {
    if (keys["arrowup"] || keys["w"]) player.y -= player.speed;
    if (keys["arrowdown"] || keys["s"]) player.y += player.speed;
    if (keys["arrowleft"] || keys["a"]) player.x -= player.speed;
    if (keys["arrowright"] || keys["d"]) player.x += player.speed;

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
                player.r += 0.3;
                food[i] = {
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    r: Math.random() * 8 + 2
                };
            } else {
                player.r = 10; // reset if hit bigger object
            }
        }
    }

    document.getElementById("size").innerText = player.r.toFixed(1);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // draw food
    for (let f of food) {
        ctx.beginPath();
        ctx.fillStyle = "#4ade80";
        ctx.arc(f.x, f.y, f.r, 0, Math.PI*2);
        ctx.fill();
    }

    // draw player hole
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
