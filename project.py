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

# --- AI-POWERED STRESS RELIEF PLANNER ---
elif page == "Stress Relief Plans":
    import pandas as pd

    st.header("💖 AI Stress Relief Planner")
    st.write("✨ Get a personalized, actionable plan — whether it’s time, money, study, or emotional stress 🌿")

    # --- Step 1: Input Stress Reason ---
    user_stress = st.text_input("💭 What’s stressing you out today?",
                                placeholder="e.g., time management, money problems, study pressure...")

    if user_stress:
        user_stress_lower = user_stress.lower()

        # Detect stress type
        if "time" in user_stress_lower:
            stress_type = "time_management"
            st.info("🕒 Detected stress type: Time Management")
        elif "money" in user_stress_lower or "finance" in user_stress_lower:
            stress_type = "money_management"
            st.info("💰 Detected stress type: Money Management")
        elif "study" in user_stress_lower or "exam" in user_stress_lower:
            stress_type = "study_stress"
            st.info("📚 Detected stress type: Study Stress")
        elif "relationship" in user_stress_lower or "family" in user_stress_lower:
            stress_type = "emotional_stress"
            st.info("💞 Detected stress type: Emotional Stress")
        else:
            stress_type = "general"
            st.info("🌿 Detected stress type: General Stress")

        # --- Step 2: Interactive Follow-ups ---
        st.divider()

        if stress_type == "time_management":
            st.subheader("🕒 Build Your Day Plan")

            hours = st.number_input("How many hours do you have today?", 1, 24, 10)
            activities = st.text_area("List your activities (one per line):",
                                      placeholder="e.g.\nStudy\nGym\nAssignments\nRelax\nDinner")
            if st.button("✨ Generate My Time Schedule"):
                if activities.strip():
                    activity_list = [a.strip() for a in activities.split("\n") if a.strip()]
                    priority = st.selectbox("Which is your top priority?", activity_list)
                    time_per_activity = round(hours / len(activity_list), 1)

                    plan = pd.DataFrame({
                        "Activity": activity_list,
                        "Allocated Time (hrs)": [time_per_activity] * len(activity_list),
                        "Priority": ["⭐" if a == priority else "" for a in activity_list]
                    })

                    st.success("✅ Here's your balanced day plan:")
                    st.dataframe(plan, use_container_width=True)

                    csv = plan.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download Plan as CSV", csv, "day_plan.csv", "text/csv")

        elif stress_type == "money_management":
            st.subheader("💰 Build Your Budget Plan")

            income = st.number_input("Enter your monthly income (₹):", min_value=0, step=1000)
            essentials = st.slider("Essentials (rent, food, bills) %", 0, 100, 50)
            savings = st.slider("Savings & Investments %", 0, 100, 20)
            leisure = st.slider("Leisure & Others %", 0, 100, 15)

            if st.button("✨ Generate My Budget Plan"):
                other = 100 - (essentials + savings + leisure)
                budget = pd.DataFrame({
                    "Category": ["Essentials", "Savings", "Leisure", "Others"],
                    "Percentage": [essentials, savings, leisure, other],
                    "Amount (₹)": [
                        income * essentials / 100,
                        income * savings / 100,
                        income * leisure / 100,
                        income * other / 100
                    ]
                })

                st.success("💡 Here’s your smart budget distribution:")
                st.dataframe(budget, use_container_width=True)

                csv = budget.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Budget as CSV", csv, "budget_plan.csv", "text/csv")

        elif stress_type == "study_stress":
            st.subheader("📚 Study Focus Plan")

            total_hours = st.number_input("Total study hours available today:", 1, 24, 6)
            subjects = st.text_area("Enter subjects or topics (one per line):",
                                    placeholder="e.g.\nMath\nPhysics\nCoding")
            if st.button("🧠 Generate Study Schedule"):
                if subjects.strip():
                    subject_list = [s.strip() for s in subjects.split("\n") if s.strip()]
                    per_subject = round(total_hours / len(subject_list), 1)

                    plan = pd.DataFrame({
                        "Subject": subject_list,
                        "Study Time (hrs)": [per_subject] * len(subject_list)
                    })

                    st.success("✅ Here’s your structured study plan:")
                    st.dataframe(plan, use_container_width=True)

                    csv = plan.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download Study Plan", csv, "study_plan.csv", "text/csv")

        elif stress_type == "emotional_stress":
            st.subheader("💞 Emotional Balance Plan")

            st.markdown("""
                - 🌤️ Start your day with 10 minutes of deep breathing  
                - ✍️ Journal 3 thoughts or feelings without judgment  
                - ☎️ Talk to one trusted person  
                - 🌿 Go for a 15-minute walk without your phone  
                - 💤 Sleep at least 7 hours tonight  
            """)
            st.info("💖 Remember: expressing emotions is a sign of strength, not weakness.")

        else:
            st.subheader("🌿 General Stress Relief Plan")
            st.markdown("""
                - 🧘 Take a 5-minute break and breathe deeply  
                - 📅 Write 3 simple tasks for today and finish one first  
                - ☕ Have water or tea mindfully  
                - 🎧 Play calming music for 10 minutes  
                - ✨ Write one thing you’re grateful for today  
            """)


# ===============================================================
# 💼 PAID SESSIONS (Improved)
# ===============================================================
elif page == "Paid Sessions":
    st.header("💼 Premium Stress-Relief Sessions (₹100)")
    st.write("Book a 1-on-1 guided session with our certified facilitators. 🌿")

    # Intro section
    st.markdown("""
    💖 **How it works:**
    1. Browse the available facilitators below 👇  
    2. Scan the QR code to pay ₹100 via Google Pay  
    3. After payment, click **‘Confirm Booking’** and contact the facilitator for scheduling  
    """)

    # QR image URL (raw GitHub version)
    qr_url = "https://raw.githubusercontent.com/Namantyagi18/Project/main/qr%20code.jpg"

    # Facilitator profiles
    trainers = [
        {"name": "Naman", "expertise": "Stress Management & Positive Mindset"},
        {"name": "Akshay", "expertise": "Mindfulness & Breathing Techniques"},
        {"name": "Akshat", "expertise": "Work-Life Balance Coaching"},
        {"name": "Arjun", "expertise": "Guided Relaxation & Emotional Healing"},
        {"name": "Brahmliv Kaur", "expertise": "Emotional Clarity & Self-Compassion"},
    ]

    # Show each trainer in a card layout
    for t in trainers:
        with st.expander(f"✨ {t['name']} — {t['expertise']}"):
            col1, col2 = st.columns([0.3, 0.7])
            with col1:
                try:
                    st.image(qr_url, width=180, caption="📱 Scan this Google Pay QR (₹100)")
                except Exception:
                    st.warning("⚠️ QR Image not available right now. Please contact the facilitator directly.")
            with col2:
                st.markdown(f"**Facilitator:** {t['name']}")
                st.markdown(f"**Expertise:** {t['expertise']}")
                st.markdown("**Session Fee:** ₹100 / 30 minutes")
                st.markdown("**Mode:** Google Meet / WhatsApp Call")

                name = st.text_input(f"Enter your name for booking with {t['name']}", key=f"name_{t['name']}")
                contact = st.text_input(f"Enter your contact number", key=f"contact_{t['name']}")

                if st.button(f"✅ Confirm Booking with {t['name']}", key=f"confirm_{t['name']}"):
                    if name.strip() and contact.strip():
                        st.success(f"🎉 {name}, your booking with **{t['name']}** is confirmed! They will contact you soon.")
                        st.info(f"📞 Contact {t['name']} at: +91-9627216110")
                        booking_data = f"""
                        Name: {name}
                        Contact: {contact}
                        Facilitator: {t['name']}
                        Expertise: {t['expertise']}
                        Fee: ₹100
                        """
                        st.download_button("📥 Download Booking Receipt", booking_data, "booking_info.txt")
                    else:
                        st.warning("Please enter your name and contact number to confirm booking.")
