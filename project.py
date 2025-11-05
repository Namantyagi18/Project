import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Digital Wellness Toolkit", page_icon="🌱", layout="wide")

st.title("🌱 Digital Wellness Toolkit")
st.markdown("#### The Silent Struggle — Manage stress, track mood, and connect with support circles.")

# Sidebar Navigation
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
    st.write("Add, track, and complete your daily tasks with motivation!")

    # Initialize session state
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    if "last_completed_count" not in st.session_state:
        st.session_state.last_completed_count = 0

    # --- Add new tasks (multiple support) ---
    with st.form("task_form", clear_on_submit=True):
        st.markdown("### ✍️ Add New Tasks")
        new_tasks = st.text_area("Enter one or more tasks (each on a new line):")
        add_task = st.form_submit_button("➕ Add Task(s)")
        if add_task and new_tasks.strip():
            task_list = [t.strip() for t in new_tasks.split("\n") if t.strip()]
            for t in task_list:
                st.session_state.tasks.append({
                    "task": t,
                    "completed": False,
                    "date": datetime.date.today().strftime("%d-%m-%Y"),
                    "time": datetime.datetime.now().strftime("%I:%M %p")
                })
            st.success(f"✅ Added {len(task_list)} new task(s)!")

    # --- Display tasks ---
    if st.session_state.tasks:
        st.subheader("📋 Your Tasks")
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

        total_tasks = len(st.session_state.tasks)
        pending_tasks = total_tasks - completed_count

        # --- Detect newly completed tasks ---
        if completed_count > st.session_state.last_completed_count:
            new_done = completed_count - st.session_state.last_completed_count
            st.success(f"🎉 Great! You completed {new_done} task{'s' if new_done > 1 else ''}!")
        st.session_state.last_completed_count = completed_count

        # --- Motivational feedback ---
        st.divider()
        if completed_count == 0:
            st.info(f"📝 You have {pending_tasks} pending tasks. Let's get started!")
        elif completed_count < total_tasks:
            st.success(f"🎯 Great job! You’ve completed {completed_count} out of {total_tasks} tasks. Keep going!")
        else:
            st.balloons()
            st.success("🌟 Amazing! You completed all your tasks for today!")

        # --- Clear all tasks button ---
        if st.button("🗑️ Clear All Tasks"):
            st.session_state.tasks.clear()
            st.session_state.last_completed_count = 0
            st.warning("All tasks cleared!")
            st.rerun()
    else:
        st.info("No tasks added yet. Add your first task above ⬆️")

# --- Mood Tracker ---
elif page == "Mood Tracker":
    st.header("😊 Mood Tracker")
    st.write("Log your current mood and view trends.")
    if "mood_data" not in st.session_state:
        st.session_state.mood_data = pd.DataFrame(columns=["Time", "Mood"])

    mood = st.radio("Select your current mood:", ["😊 Happy", "😐 Neutral", "☹️ Sad"], horizontal=True)
    if st.button("Log Mood"):
        new_entry = {"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Mood": mood}
        st.session_state.mood_data = pd.concat(
            [st.session_state.mood_data, pd.DataFrame([new_entry])],
            ignore_index=True
        )
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

# --- Peer Support Circles ---
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
            st.image(r"C:\Users\Naman\Desktop\Project\qr code.jpg", width=180, caption="Scan this Google Pay QR (₹100)")
            st.write("After payment, contact the facilitator to confirm your session timing.")
            if st.button(f"Contact {t['name']}", key=t['name']):
                st.info(f"Contact {t['name']} at: +91-XXXXXXXXXX")
