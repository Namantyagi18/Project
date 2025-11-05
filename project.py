import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

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

    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    if "last_completed_count" not in st.session_state:
        st.session_state.last_completed_count = 0

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

        if completed_count > st.session_state.last_completed_count:
            new_done = completed_count - st.session_state.last_completed_count
            st.success(f"🎉 Great! You completed {new_done} task{'s' if new_done > 1 else ''}!")
        st.session_state.last_completed_count = completed_count

        st.divider()
        if completed_count == 0:
            st.info(f"📝 You have {pending_tasks} pending tasks. Let's get started!")
        elif completed_count < total_tasks:
            st.success(f"🎯 Great job! You’ve completed {completed_count} out of {total_tasks} tasks. Keep going!")
        else:
            st.balloons()
            st.success("🌟 Amazing! You completed all your tasks for today!")

        if st.button("🗑️ Clear All Tasks"):
            st.session_state.tasks.clear()
            st.session_state.last_completed_count = 0
            st.warning("All tasks cleared!")
            st.rerun()
    else:
        st.info("No tasks added yet. Add your first task above ⬆️")

# --- Mood Tracker ---
elif page == "Mood Tracker":

    # 🌈 Stylish background + button CSS
    st.markdown("""
        <style>
        body {
            background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        }
        .stButton>button {
            border-radius: 15px;
            height: 4em;
            width: 100%;
            background: linear-gradient(135deg, #a1ffce 0%, #faffd1 100%);
            border: none;
            color: #333;
            font-size: 1.3em;
            font-weight: 600;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0px 6px 14px rgba(0,0,0,0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center; color:#006400;'>🧘 Mood Tracker</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Log your daily emotions and visualize your inner journey 🌿</p>", unsafe_allow_html=True)

    if "mood_data" not in st.session_state:
        st.session_state.mood_data = pd.DataFrame(columns=["Time", "Mood", "Note"])

    st.markdown("### ✨ How are you feeling right now?")
    mood_col1, mood_col2, mood_col3 = st.columns(3)
    with mood_col1:
        happy = st.button("😊 Happy")
    with mood_col2:
        neutral = st.button("😐 Neutral")
    with mood_col3:
        sad = st.button("☹️ Sad")

    note = st.text_area("💭 Write about how you feel (optional):", placeholder="e.g., Feeling motivated after gym or a bit tired from studies...")
    current_time = datetime.datetime.now().strftime("%I:%M %p")

    if happy:
        mood, msg, color = "😊 Happy", "🌞 You’re shining bright today!", "#A3E4D7"
    elif neutral:
        mood, msg, color = "😐 Neutral", "🌤️ Balanced mood — take a mindful pause.", "#F9E79F"
    elif sad:
        mood, msg, color = "☹️ Sad", "💖 It’s okay to feel down — give yourself kindness.", "#F5B7B1"
    else:
        mood, msg, color = None, None, None

    if mood:
        new_entry = {"Time": current_time, "Mood": mood, "Note": note}
        st.session_state.mood_data = pd.concat([st.session_state.mood_data, pd.DataFrame([new_entry])], ignore_index=True)
        st.markdown(f"<div style='background-color:{color}; padding:15px; border-radius:10px; text-align:center; font-size:1.1em; font-weight:500;'>{msg}</div>", unsafe_allow_html=True)

    if not st.session_state.mood_data.empty:
        st.markdown("---")
        st.markdown("<h4 style='text-align:center;'>📈 Your Mood Flow</h4>", unsafe_allow_html=True)

        mood_map = {"😊 Happy": 3, "😐 Neutral": 2, "☹️ Sad": 1}
        color_map = {"😊 Happy": "#2ECC71", "😐 Neutral": "#F1C40F", "☹️ Sad": "#E74C3C"}
        mood_df = st.session_state.mood_data.copy()
        mood_df["Mood_Value"] = mood_df["Mood"].map(mood_map)

        fig = px.line(mood_df, x="Time", y="Mood_Value", text="Mood", markers=True,
                      color="Mood", color_discrete_map=color_map, title="Emotional Flow Over Time")

        fig.update_traces(textposition="top center", line_shape="spline", line=dict(width=4),
                          marker=dict(size=15, line=dict(width=2, color="white")))
        fig.update_yaxes(tickvals=[1, 2, 3], ticktext=["☹️ Sad", "😐 Neutral", "😊 Happy"], title="Mood Level")
        fig.update_layout(xaxis_title="Time Logged", yaxis_title="Mood", template="plotly_white",
                          plot_bgcolor="rgba(245,255,245,0.9)", paper_bgcolor="rgba(255,255,255,0)",
                          font=dict(family="Arial", size=14), title_font=dict(size=20, color="#2E8B57"))
        st.plotly_chart(fig, use_container_width=True)

        # --- Mood Summary Section ---
        st.markdown("---")
        st.markdown("<h4 style='text-align:center;'>📊 Mood Summary</h4>", unsafe_allow_html=True)

        mood_counts = mood_df["Mood"].value_counts().reset_index()
        mood_counts.columns = ["Mood", "Count"]

        col1, col2, col3 = st.columns(3)
        col1.metric("😊 Happy", int(mood_counts[mood_counts["Mood"] == "😊 Happy"]["Count"].sum()))
        col2.metric("😐 Neutral", int(mood_counts[mood_counts["Mood"] == "😐 Neutral"]["Count"].sum()))
        col3.metric("☹️ Sad", int(mood_counts[mood_counts["Mood"] == "☹️ Sad"]["Count"].sum()))

        st.markdown("### 🎭 Mood Frequency Chart")
        fig2 = px.bar(mood_counts, x="Mood", y="Count", color="Mood", color_discrete_map=color_map,
                      text="Count", title="Number of Times Each Mood Logged")
        fig2.update_traces(textposition="outside", marker=dict(line=dict(width=2, color="white")),
                           hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>")
        fig2.update_layout(xaxis_title="Mood Type", yaxis_title="Count", template="plotly_white",
                           plot_bgcolor="rgba(245,255,245,0.9)", paper_bgcolor="rgba(255,255,255,0)",
                           title_font=dict(size=20, color="#2E8B57"))
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.subheader("🗒️ Mood Journal")
        st.dataframe(mood_df[["Time", "Mood", "Note"]], use_container_width=True, height=200)

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
            st.image(r"https://github.com/Namantyagi18/Project/blob/main/qr%20code.jpg", width=180,
                     caption="Scan this Google Pay QR (₹100)")
            st.write("After payment, contact the facilitator to confirm your session timing.")
            if st.button(f"Contact {t['name']}", key=t['name']):
                st.info(f"Contact {t['name']} at: +91-9627216110")
                st.success("Session booked! Looking forward to helping you relax and rejuvenate. 🌿")
