import streamlit as st
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Treasure Escape",
    page_icon="🏴‍☠️",
    layout="centered"
)

# ---------------- CUSTOM HTML/CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.main-title {
    text-align: center;
    color: #facc15;
    font-size: 50px;
    font-weight: bold;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from {
        text-shadow: 0 0 10px #facc15;
    }
    to {
        text-shadow: 0 0 25px #fde047;
    }
}

.card {
    background: linear-gradient(135deg, #1e293b, #334155);
    padding: 20px;
    border-radius: 20px;
    color: white;
    box-shadow: 0 0 20px rgba(255,255,255,0.1);
    margin-top: 20px;
}

.treasure {
    font-size: 80px;
    text-align: center;
    animation: bounce 1s infinite;
}

@keyframes bounce {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.footer {
    text-align: center;
    margin-top: 40px;
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="main-title">🏴‍☠️ Treasure Escape</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
<h3>Mission</h3>
<p>You are trapped inside a mysterious cave. One of the 3 doors contains treasure.
The other two contain traps. Choose wisely.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "wins" not in st.session_state:
    st.session_state.wins = 0

if "losses" not in st.session_state:
    st.session_state.losses = 0

# ---------------- GAME LOGIC ----------------
treasure_door = random.randint(1, 3)

st.subheader("Choose a Door")

col1, col2, col3 = st.columns(3)

choice = None

with col1:
    if st.button("🚪 Door 1"):
        choice = 1

with col2:
    if st.button("🚪 Door 2"):
        choice = 2

with col3:
    if st.button("🚪 Door 3"):
        choice = 3

# ---------------- RESULT ----------------
if choice:
    with st.spinner("Opening the door..."):
        time.sleep(1.5)

    if choice == treasure_door:
        st.session_state.wins += 1

        st.markdown("""
        <div class="card">
            <div class="treasure">💰</div>
            <h2 style="text-align:center;color:#4ade80;">YOU FOUND THE TREASURE!</h2>
        </div>
        """, unsafe_allow_html=True)

        st.balloons()

    else:
        st.session_state.losses += 1

        st.markdown("""
        <div class="card">
            <h2 style="text-align:center;color:#f87171;">💀 TRAP ACTIVATED!</h2>
            <p style="text-align:center;">Better luck next time.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------- SCOREBOARD ----------------
st.markdown(f"""
<div class="card">
<h3>📊 Scoreboard</h3>
<p>Wins: <b>{st.session_state.wins}</b></p>
<p>Losses: <b>{st.session_state.losses}</b></p>
</div>
""", unsafe_allow_html=True)

# ---------------- BONUS HTML ELEMENT ----------------
st.markdown("""
<div class="footer">
<hr>
<p>Made with ❤️ using Streamlit + HTML + CSS</p>
</div>
""", unsafe_allow_html=True)
