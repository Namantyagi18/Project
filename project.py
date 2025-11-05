import streamlit as st
import pandas as pd
import datetime

# ===============================================================
# 🌈 PAGE CONFIGURATION
# ===============================================================
st.set_page_config(page_title="Digital Wellness Toolkit", page_icon="🌱", layout="wide")

# --- GLOBAL CUSTOM STYLES ---
st.markdown("""
<style>
/* Background gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
    font-family: 'Poppins', sans-serif;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #a8edea 0%, #fed6e3 100%);
    color: #333;
    border-right: 2px solid #ccc;
}

/* Titles */
h1, h2, h3 {
    text-align: center;
    color: #2c3e50;
    font-weight: 600;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 16px;
    transition: 0.3s;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
    transform: scale(1.03);
}

/* Info boxes */
.stAlert {
    border-radius: 10px;
    font-size: 16px;
}

/* Divider */
hr {
    border: 1px solid #aaa;
    margin-top: 20px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===============================================================
# 🌱 APP TITLE
# ===============================================================
st.title("🌱 **Digital Wellness Toolkit**")
st.markdown("<h4 style='text-align:center;color:#555;'>✨ The Silent Struggle — Manage stress, track mood, and connect with support circles ✨</h4>", unsafe_allow_html=True)
st.write("")

# ===============================================================
# 🧭 SIDEBAR NAVIGATION
# ===============================================================
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Choose a section:", [
    "Task Manager",
    "Mood Tracker",
    "Wellness Tips",
    "Peer Support Circles",
    "Stress Relief Plans",
    "Paid Sessions"
])

# ===============================================================
# 🕒 TASK MANAGER
# ===============================================================
if page == "Task Manager":
    st.subheader("🕒 Task Manager — Stay Organized and Motivated!")

    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    if "last_completed_count" not in st.session_state:
        st.session_state.last_completed_count = 0

    with st.form("task_form", clear_on_submit=True):
        st.markdown("### ✍️ Add New Tasks")
        new_tasks = st.text_area("Enter one or more tasks (each on a new line):", placeholder="e.g. Complete project, call friend, workout...")
        add_task = st.form_submit_button("➕ Add Task(s)")
        if add_task and new_tasks.strip():
            for t in new_tasks.split("\n"):
                if t.strip():
                    st.session_state.tasks.append({
                        "task": t.strip(),
                        "completed": False,
                        "date": datetime.date.today().strftime("%d-%m-%Y"),
                        "time": datetime.datetime.now().strftime("%I:%M %p")
                    })
            st.success("✅ Task(s) added successfully!")

    if st.session_state.tasks:
        st.markdown("### 📋 Your Task List")
        completed_count = 0

        for i, t in enumerate(st.session_state.tasks):
            cols = st.columns([0.07, 0.63, 0.3])
            done = cols[0].checkbox("", value=t["completed"], key=f"task_{i}")
            cols[1].write(f"**{t['task']}**  \n📅 *{t['date']}* | 🕒 *{t['time']}*")
            if done:
                st.session_state.tasks[i]["completed"] = True
                cols[2].success("✔️ Completed")
                completed_count += 1
            else:
                st.session_state.tasks[i]["completed"] = False
                cols[2].warning("⏳ Pending")

        total = len(st.session_state.tasks)
        st.divider()
        if completed_count == total:
            st.balloons()
            st.success("🌟 Amazing! You’ve completed all your tasks for today!")
        elif completed_count > 0:
            st.success(f"🎯 You’ve completed {completed_count}/{total} tasks — Keep it up!")
        else:
            st.info(f"📝 You have {total} pending tasks. Let’s get started!")

        if st.button("🗑️ Clear All Tasks"):
            st.session_state.tasks.clear()
            st.session_state.last_completed_count = 0
            st.warning("All tasks cleared!")
            st.rerun()
    else:
        st.info("No tasks yet — add your first one above! 🌱")

# ===============================================================
# 😊 MOOD TRACKER
# ===============================================================
elif page == "Mood Tracker":
    st.subheader("😊 Mood Tracker — Reflect Your Daily Feelings")

    if "mood_data" not in st.session_state:
        st.session_state.mood_data = pd.DataFrame(columns=["Time", "Mood"])

    mood = st.radio("Select your current mood:", ["😊 Happy", "😐 Neutral", "☹️ Sad"], horizontal=True)
    if st.button("🧠 Log Mood"):
        new_entry = {"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Mood": mood}
        st.session_state.mood_data = pd.concat([st.session_state.mood_data, pd.DataFrame([new_entry])], ignore_index=True)
        st.success(f"💾 Mood '{mood}' logged successfully!")

    if not st.session_state.mood_data.empty:
        st.markdown("### 📊 Mood Trend")
        mood_chart = st.session_state.mood_data["Mood"].map({"😊 Happy": 3, "😐 Neutral": 2, "☹️ Sad": 1})
        st.area_chart(mood_chart)

# ===============================================================
# 💬 WELLNESS TIPS
# ===============================================================
elif page == "Wellness Tips":
    st.subheader("💬 Daily Wellness Tip — A Little Reminder 🌿")
    tips = [
        "🌞 Step outside and take 5 deep breaths.",
        "🧘 Try 5 minutes of meditation — quiet minds create calm hearts.",
        "🎧 Listen to your favorite calming song.",
        "🪴 Water your plants or tidy your space for clarity.",
        "💖 Send a thank-you message to someone today."
    ]
    st.success(f"✨ {tips[datetime.datetime.now().second % len(tips)]}")

# ===============================================================
# 🤝 PEER SUPPORT CIRCLES
# ===============================================================
elif page == "Peer Support Circles":
    st.subheader("🤝 Guided Peer Support Circles — Grow Together 🌸")
    circles = [
        {"name": "🌿 Stress Support Circle", "members": 12, "topic": "Managing academic stress"},
        {"name": "🔥 Productivity Boosters", "members": 9, "topic": "Focus and motivation"},
        {"name": "🌙 Calm Minds", "members": 15, "topic": "Mindfulness and relaxation"}
    ]
    for c in circles:
        with st.expander(f"{c['name']} ({c['members']} members)"):
            st.markdown(f"**Topic:** {c['topic']}")
            if st.button(f"Join {c['name']}", key=c['name']):
                st.success(f"🎉 You’ve joined {c['name']}! Welcome aboard! 💬")

# ===============================================================
# 💖 STRESS RELIEF PLANS
# ===============================================================
elif page == "Stress Relief Plans":
    st.subheader("💖 Personalized Stress Relief Plans 🌸")
    current_mood = st.radio("How are you feeling today?", ["😊 Happy", "😐 Neutral", "☹️ Sad"], horizontal=True)
    plans = {
        "😊 Happy": "🌞 Keep journaling and stay active — share your good vibes with someone today!",
        "😐 Neutral": "🌿 Try light meditation, hydrate well, and spend time offline.",
        "☹️ Sad": "💖 Take it slow — listen to calm music, talk to a friend, or take a warm shower."
    }
    st.info(plans[current_mood])

# ===============================================================
# 💼 PAID SESSIONS (Polished UI)
# ===============================================================
elif page == "Paid Sessions":
    st.subheader("💼 Premium Stress-Relief Sessions (₹100)")
    st.markdown("""
    💖 **How it works:**
    1️⃣ Browse our certified facilitators below  
    2️⃣ Scan the QR to pay ₹100  
    3️⃣ Confirm your booking and relax 🌿
    """)

    qr_url = "https://raw.githubusercontent.com/Namantyagi18/Project/main/qr%20code.jpg"

    trainers = [
        {"name": "Naman", "expertise": "Stress Management & Positive Mindset"},
        {"name": "Akshay", "expertise": "Mindfulness & Breathing Techniques"},
        {"name": "Akshat", "expertise": "Work-Life Balance Coaching"},
        {"name": "Arjun", "expertise": "Guided Relaxation & Emotional Healing"},
        {"name": "Brahmliv Kaur", "expertise": "Emotional Clarity & Self-Compassion"},
    ]

    for t in trainers:
        with st.expander(f"✨ {t['name']} — {t['expertise']}"):
            col1, col2 = st.columns([0.3, 0.7])
            with col1:
                try:
                    st.image(qr_url, width=160, caption="📱 Scan this QR (₹100)")
                except Exception:
                    st.warning("⚠️ QR not available right now.")
            with col2:
                st.markdown(f"**Facilitator:** {t['name']}  \n**Expertise:** {t['expertise']}  \n**Fee:** ₹100  \n**Mode:** Google Meet / WhatsApp")
                name = st.text_input(f"Enter your name to book with {t['name']}", key=f"name_{t['name']}")
                contact = st.text_input(f"Enter contact number", key=f"contact_{t['name']}")
                if st.button(f"✅ Confirm Booking with {t['name']}", key=f"confirm_{t['name']}"):
                    if name.strip() and contact.strip():
                        st.success(f"🎉 Booking confirmed for {name} with **{t['name']}**! They’ll reach out soon 🌼")
                    else:
                        st.warning("Please enter both name and contact to confirm booking.")
