import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Digital Wellness Toolkit", page_icon="🌱", layout="wide")

st.title("🌱 Digital Wellness Toolkit")
st.markdown("#### The Silent Struggle — Manage stress, track mood, and connect with support circles.")

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", [
    "Task Manager",
    "Mood Tracker",
    "Wellness Tips",
    "Peer Support Circles",
    "Stress Relief Plans",
    "Paid Sessions"
])

# --- Task Manager ---
if page == "Task Manager":
    st.header("🕒 Task Manager")
    st.write("Add and prioritize your daily tasks.")
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    task_input = st.text_input("Enter a new task:")
    if st.button("Add Task"):
        if task_input.strip():
            st.session_state.tasks.append({"task": task_input, "done": False})
    for i, t in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([0.8, 0.2])
        if col1.checkbox(t["task"], value=t["done"], key=f"task_{i}"):
            st.session_state.tasks[i]["done"] = True
        if col2.button("❌", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()

# --- Mood Tracker ---
elif page == "Mood Tracker":
    st.header("😊 Mood Tracker")
    st.write("Log your current mood and view trends.")
    if "mood_data" not in st.session_state:
        st.session_state.mood_data = pd.DataFrame(columns=["Time", "Mood"])

    mood = st.radio("Select your current mood:", ["😊 Happy", "😐 Neutral", "☹️ Sad"], horizontal=True)
    if st.button("Log Mood"):
        new_entry = {"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Mood": mood}
        st.session_state.mood_data = pd.concat([st.session_state.mood_data, pd.DataFrame([new_entry])], ignore_index=True)
        st.success("Mood logged successfully!")

    if not st.session_state.mood_data.empty:
        st.line_chart(st.session_state.mood_data["Mood"].map({"😊 Happy": 3, "😐 Neutral": 2, "☹️ Sad": 1}))

# --- Wellness Tips ---
elif page == "Wellness Tips":
    st.header("💬 Wellness Tips")
    tips = [
        "Take a short walk and stretch. 🚶‍♀️",
        "Remember to breathe deeply for a minute. 🌬️",
        "Organize your tasks one at a time. ✅",
        "Unplug for 10 minutes. 🌿",
        "Smile! You’re doing great. 😊"
    ]
    st.info(f"✨ {tips[pd.Timestamp.now().second % len(tips)]}")

# --- Peer Circles ---
elif page == "Peer Support Circles":
    st.header("🤝 Guided Peer Support Circles")
    circles = [
        {"name": "Stress Support Circle", "members": 12, "topic": "Managing academic stress"},
        {"name": "Productivity Boosters", "members": 9, "topic": "Focus and motivation"},
        {"name": "Calm Minds", "members": 15, "topic": "Mindfulness and relaxation"}
    ]
    for c in circles:
        with st.expander(f"{c['name']} ({c['members']} members)"):
            st.write(f"**Topic:** {c['topic']}")
            if st.button(f"Join {c['name']}", key=c['name']):
                st.success(f"You have joined {c['name']}!")

# --- Stress Relief Plans ---
elif page == "Stress Relief Plans":
    st.header("💖 Personalized Stress Relief Plans")
    current_mood = st.radio("How are you feeling today?", ["😊 Happy", "😐 Neutral", "☹️ Sad"], horizontal=True)
    plans = {
        "😊 Happy": "Keep journaling and stay active! Maintain your positive energy by sharing gratitude notes. 🌞",
        "😐 Neutral": "Try a guided meditation or short breathing session to refresh your mind. 🌿",
        "☹️ Sad": "Listen to calm music, connect with friends, or journal your thoughts. Take small self-care steps. 💖"
    }
    st.success(plans[current_mood])

# --- Paid Sessions ---
elif page == "Paid Sessions":
    st.header("💼 Paid Stress-Relief Sessions (₹100)")
    st.write("Book a 1-on-1 guided stress relief session with one of our facilitators. Payment through Google Pay QR below 👇")

    trainers = [
        {"name": "Naman", "expertise": "Stress Management & Positive Mindset"},
        {"name": "Akshay", "expertise": "Mindfulness & Breathing Techniques"},
        {"name": "Akshat", "expertise": "Work-Life Balance Coaching"},
        {"name": "Arjun", "expertise": "Guided Relaxation & Emotional Healing"},
        {"name": "Brahmliv Kaur", "expertise": "Emotional Clarity & Self-Compassion Sessions"},
    ]

    for t in trainers:
        with st.expander(f"{t['name']} — {t['expertise']}"):
            st.image("C:\Users\Naman\Desktop\Project\qr code.jpg", width=180, caption="Scan this Google Pay QR (₹100)")
            st.write("After payment, contact the facilitator to confirm your session timing.")

   
