import streamlit as st
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Treasure Escape",
    page_icon="🏴‍☠️",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "treasure_door" not in st.session_state:
    st.session_state.treasure_door = random.randint(1, 3)
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "message" not in st.session_state:
    st.session_state.message = ""

# ---------------- CSS + HTML THEME ----------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f172a, #020617);
}

/* HEADER BANNER */
.banner {
    text-align: center;
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(90deg, #1e293b, #334155, #1e293b);
    color: #facc15;
    font-size: 40px;
    font-weight: bold;
    letter-spacing: 2px;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px #facc15; }
    to { text-shadow: 0 0 30px #fde047; }
}

/* GAME FRAME */
.frame {
    border: 2px solid #334155;
    padding: 20px;
    border-radius: 20px;
    margin-top: 20px;
    background: rgba(30,41,59,0.6);
}

/* DOOR CARD */
.door {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(135deg, #1e293b, #0f172a);
    text-align: center;
    font-size: 22px;
    color: white;
    cursor: pointer;
    transition: 0.3s;
    border: 2px solid #334155;
}

.door:hover {
    transform: scale(1.05);
    border-color: #facc15;
}

/* RESULT BOX */
.result-win {
    background: #14532d;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: #4ade80;
}

.result-lose {
    background: #450a0a;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: #f87171;
}

/* SCORE BAR */
.bar {
    height: 20px;
    background: #334155;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 10px;
}

.fill {
    height: 100%;
    background: linear-gradient(90deg, #22c55e, #eab308);
}

/* FOOTER */
.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="banner">
🏴‍☠️ TREASURE ESCAPE 🏴‍☠️
</div>
""", unsafe_allow_html=True)

# ---------------- GAME FRAME ----------------
st.markdown('<div class="frame">', unsafe_allow_html=True)

st.markdown("""
<h3 style="color:#e2e8f0;text-align:center;">
One door hides treasure. Two hide traps.
</h3>
""", unsafe_allow_html=True)

# ---------------- GAME LOGIC ----------------
if not st.session_state.game_over:

    col1, col2, col3 = st.columns(3)

    def handle_choice(choice):
        st.session_state.game_over = True

        if choice == st.session_state.treasure_door:
            st.session_state.wins += 1
            st.session_state.message = "win"
        else:
            st.session_state.losses += 1
            st.session_state.message = "lose"

    with col1:
        if st.button("🚪 Door 1"):
            handle_choice(1)

    with col2:
        if st.button("🚪 Door 2"):
            handle_choice(2)

    with col3:
        if st.button("🚪 Door 3"):
            handle_choice(3)

# ---------------- RESULT ----------------
if st.session_state.game_over:

    time.sleep(0.5)

    if st.session_state.message == "win":
        st.markdown("""
        <div class="result-win">
            <h2>💰 YOU FOUND THE TREASURE!</h2>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-lose">
            <h2>💀 TRAP ACTIVATED!</h2>
            <p>The treasure was behind Door {st.session_state.treasure_door}</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔄 Play Again"):
        st.session_state.treasure_door = random.randint(1, 3)
        st.session_state.game_over = False
        st.rerun()

# ---------------- SCOREBOARD ----------------
total = st.session_state.wins + st.session_state.losses
win_ratio = (st.session_state.wins / total) * 100 if total > 0 else 0

st.markdown(f"""
<h4 style="color:white;">📊 Scoreboard</h4>

Wins: <b>{st.session_state.wins}</b><br>
Losses: <b>{st.session_state.losses}</b><br>

<div class="bar">
    <div class="fill" style="width:{win_ratio}%"></div>
</div>

<p style="color:#94a3b8;">Win Rate: {win_ratio:.1f}%</p>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit + Advanced HTML/CSS
</div>
""", unsafe_allow_html=True)
