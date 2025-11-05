import streamlit as st
import pandas as pd
import datetime

# Page config
st.set_page_config(page_title="Digital Wellness Toolkit", page_icon="🌱", layout="wide")

# Title
st.title("🌱 Digital Wellness Toolkit")
st.markdown("#### The Silent Struggle — Manage stress, track mood, and connect with support circles.")

# Sidebar navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Task Manager",
        "Mood Tracker",
        "Wellness Tips",
        "Peer Support Circles",
        "Stress Relief Plans",
        "Paid Sessions",
    ],
    key="main_nav"  # ✅ unique key prevents duplicate ID error
)

# ===============================================================
# 🕒 TASK MANAGER
# ===============================================================
if page == "Task Manager":
    st.header("🕒 Task Manager")
    st.write("Add, track, and complete your daily tasks with motivation!")

    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    if "last_completed_count" not in st.session_state:
        st.session_state.last_completed_count = 0

    # Add new tasks
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

    # Display tasks
    if st.session_state.tasks:
        st.subheader("📋 Your Tasks")
        completed_count = 0
        for i, t in enumerate(st.session_state.tasks):
            cols = st.columns([0.07, 0.6, 0.33])
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

        st.divider()
        if completed_count == 0:
            st.info(f"📝 You have {pending_tasks} pending tasks. Let's get started!")
        elif completed_count < total_tasks:
            st.success(f"🎯 Great job! You’ve completed {completed_count} out of {total_tasks} tasks. Keep going!")
        else:
            st.balloons()
            st.success("🌟 Amazing! You completed all your tasks for today!")

        if completed_count > st.session_state.last_completed_count:
            st.toast(f"🎉 You just completed {completed_count - st.session_state.last_completed_count} task(s)!", icon="✅")
        st.session_state.last_completed_count = completed_count

        if st.button("🗑️ Clear All Tasks"):
            st.session_state.tasks.clear()
            st.session_state.last_completed_count = 0
            st.warning("All tasks cleared!")
            st.rerun()
    else:
        st.info("No tasks added yet. Add your first task above ⬆️")

# ===============================================================
# 😊 MOOD TRACKER
# ===============================================================
elif page == "Mood Tracker":
    st.header("😊 Mood Tracker")
    st.write("Log your mood and track your emotional trends over time.")

    if "mood_data" not in st.session_state:
        st.session_state.mood_data = pd.DataFrame(columns=["Time", "Mood"])

    mood = st.radio("Select your mood:", ["😊 Happy", "😐 Neutral", "☹️ Sad"], horizontal=True)
    if st.button("Log Mood"):
        new_entry = {"Time": datetime.datetime.now().strftime("%H:%M:%S"), "Mood": mood}
        st.session_state.mood_data = pd.concat([st.session_state.mood_data, pd.DataFrame([new_entry])], ignore_index=True)
        st.success("Mood logged successfully!")

    if not st.session_state.mood_data.empty:
        st.line_chart(st.session_state.mood_data["Mood"].map({"😊 Happy": 3, "😐 Neutral": 2, "☹️ Sad": 1}))

# ===============================================================
# 💬 EMOTION-AWARE WELLNESS TIPS
# ===============================================================
elif page == "Wellness Tips":
    st.header("💬 Emotion-Aware Wellness Assistant")
    st.write("Express your emotions — get personalized wellness advice 🌿")

    emotion_text = st.text_area("💭 How do you feel today?")
    if st.button("💡 Get My Wellness Tip"):
        if not emotion_text.strip():
            st.warning("Please share your feelings first 💬")
        else:
            text = emotion_text.lower()
            mood = "neutral"
            if any(w in text for w in ["happy", "excited", "grateful"]):
                mood = "happy"
            elif any(w in text for w in ["sad", "tired", "anxious", "stressed"]):
                mood = "sad"

            if mood == "happy":
                st.success("🌞 You’re glowing! Keep spreading positivity. Maybe share a smile or do something kind today.")
            elif mood == "sad":
                st.info("💖 Take a break, breathe, and treat yourself gently. A short walk or journaling can help.")
            else:
                st.info("🌿 Stay grounded — maybe listen to soft music or make tea and take a mindful pause.")

# ===============================================================
# 🤝 PEER SUPPORT CIRCLES
# ===============================================================
elif page == "Peer Support Circles":
    st.header("🤝 Guided Peer Support Circles")
    st.markdown("Join a group that fits your current emotional need 🌱")

    circles = {
        "Stress Support Circle": ["Aarav", "Diya", "Raj"],
        "Productivity Boosters": ["Ishaan", "Tanya"],
        "Calm Minds": ["Riya", "Karan", "Ananya"]
    }

    st.subheader("✨ Describe your current feeling for a recommendation")
    feeling = st.text_area("💭 How are you feeling right now?")
    if st.button("🎯 Recommend a Circle"):
        if not feeling.strip():
            st.warning("Please describe how you feel.")
        else:
            f = feeling.lower()
            if "stress" in f or "tired" in f:
                st.success("💡 You should join **Stress Support Circle** 🌿")
            elif "motivation" in f or "focus" in f:
                st.success("💡 You should join **Productivity Boosters** 💪")
            else:
                st.success("💡 You might like **Calm Minds** for peace and mindfulness 🧘")

    st.markdown("---")
    for name, members in circles.items():
        with st.expander(f"{name} ({len(members)} members)"):
            st.write("👥 Members:", ", ".join(members))
            join_name = st.text_input(f"Enter your name to join {name}:", key=name)
            if st.button(f"Join {name}", key=f"join_{name}"):
                if join_name and join_name not in members:
                    circles[name].append(join_name)
                    st.success(f"🎉 {join_name}, welcome to {name}!")
                else:
                    st.warning("Please enter a valid name or you’re already in this circle.")

# ===============================================================
# 💖 PERSONALIZED STRESS RELIEF PLANS
# ===============================================================
elif page == "Stress Relief Plans":
    st.header("💖 Personalized Stress Relief Plans")
    st.write("Describe your stress and get a personalized plan 🌿")

    user_stress = st.text_area("💭 What's stressing you out today?")
    if st.button("🌸 Generate My Plan"):
        if not user_stress.strip():
            st.warning("Please describe your stress first.")
        else:
            text = user_stress.lower()
            if "exam" in text or "study" in text:
                st.info("🎓 Study Plan: Take 10-minute breaks, stay hydrated, and focus one topic at a time.")
            elif "work" in text or "deadline" in text:
                st.info("💼 Work Plan: Step away for 5 minutes, breathe deeply, and list top 3 priorities.")
            elif "sleep" in text or "tired" in text:
                st.info("🌙 Rest Plan: Turn off screens 30 minutes before bed and play calm music.")
            else:
                st.info("🌿 General Plan: Go for a short walk, breathe deeply, and write one good thing about today.")

# ===============================================================
# 💼 PAID SESSIONS
# ===============================================================
elif page == "Paid Sessions":
    st.header("💼 Paid Stress-Relief Sessions (₹100)")
    st.write("Book a 1-on-1 guided session. Pay via QR below 👇")

    trainers = [
        {"name": "Naman", "expertise": "Stress Management & Positive Mindset"},
        {"name": "Akshay", "expertise": "Mindfulness & Breathing Techniques"},
        {"name": "Akshat", "expertise": "Work-Life Balance Coaching"},
        {"name": "Arjun", "expertise": "Guided Relaxation & Emotional Healing"},
        {"name": "Brahmliv Kaur", "expertise": "Emotional Clarity & Self-Compassion Sessions"},
    ]

    for t in trainers:
        with st.expander(f"{t['name']} — {t['expertise']}"):
            st.image("C:/Users/Naman/Desktop/Project/qr code.jpg", width=180, caption="Scan this Google Pay QR (₹100)")
            st.write("After payment, contact the facilitator to confirm your session.")
            st.success(f"📞 Contact {t['name']} at: +91-XXXXXXXXXX" )
