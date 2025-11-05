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

# --- Emotion-Aware Wellness Tips ---
elif page == "Wellness Tips":
    st.header("💬 Emotion-Aware Wellness Assistant")
    st.write("✨ Express how you feel below — your app will understand your emotion and share a helpful wellness tip 🌿")

    st.markdown("""
        <style>
        .emotion-card {
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 1.2em;
            font-weight: 500;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
            margin-top: 20px;
            color: #333;
        }
        .happy { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
        .neutral { background: linear-gradient(135deg, #fff1eb 0%, #ace0f9 100%); }
        .sad { background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%); }
        </style>
    """, unsafe_allow_html=True)

    # User expresses emotion
    emotion_text = st.text_area("💭 Write how you feel today:", placeholder="e.g., I feel tired and anxious about my exams...")

    if st.button("💡 Get My Wellness Tip"):
        if not emotion_text.strip():
            st.warning("Please express your feelings first 💬")
        else:
            # Basic sentiment analysis (simple keyword-based)
            emotion_text_lower = emotion_text.lower()
            happy_words = ["happy", "great", "good", "excited", "joy", "grateful", "awesome"]
            sad_words = ["sad", "tired", "stressed", "depressed", "anxious", "upset", "angry", "lonely"]
            neutral_words = ["okay", "fine", "normal", "alright", "neutral"]

            mood = "neutral"
            if any(word in emotion_text_lower for word in happy_words):
                mood = "happy"
            elif any(word in emotion_text_lower for word in sad_words):
                mood = "sad"

            # Mood-based tips
            if mood == "happy":
                tips = [
                    "🌞 Keep this energy alive — share your joy with someone today!",
                    "💬 Write down 3 things that made you smile today — small joys matter.",
                    "🎵 Play your favorite upbeat song and celebrate yourself!",
                    "🌼 Use your positive energy to start something creative today!"
                ]
                selected_tip = tips[datetime.datetime.now().second % len(tips)]
                st.markdown(f"<div class='emotion-card happy'>😊 **You seem joyful!** <br><br>{selected_tip}</div>", unsafe_allow_html=True)

            elif mood == "sad":
                tips = [
                    "💖 It’s okay to rest — healing is progress too.",
                    "🌧️ Try writing down your feelings — you’ll feel lighter after.",
                    "🤍 Call a friend or listen to calming music — connection heals.",
                    "🌙 Breathe deeply and remind yourself: tough times pass, gentle soul."
                ]
                selected_tip = tips[datetime.datetime.now().second % len(tips)]
                st.markdown(f"<div class='emotion-card sad'>☁️ **You seem a bit low.** <br><br>{selected_tip}</div>", unsafe_allow_html=True)

            else:
                tips = [
                    "🌿 Take a short walk or stretch — clarity comes with motion.",
                    "☕ Make yourself a warm drink and take 5 mindful breaths.",
                    "📚 Read a quote or a short poem that inspires you.",
                    "🪷 Pause. Reflect. You’re doing just fine — one step at a time."
                ]
                selected_tip = tips[datetime.datetime.now().second % len(tips)]
                st.markdown(f"<div class='emotion-card neutral'>🌤️ **You seem calm.** <br><br>{selected_tip}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("✨ *Wellness begins with awareness — thank yourself for checking in today.* 🌸")


# --- Peer Support Circles (AI Recommendation + Interactive Join System) ---
elif page == "Peer Support Circles":
    st.header("🤝 Guided Peer Support Circles")
    st.markdown("✨ Join a circle that fits your current emotional needs or get an AI suggestion based on how you feel 💬")

    # Initialize circles and session data
    if "joined_circles" not in st.session_state:
        st.session_state.joined_circles = {}
    if "circle_members" not in st.session_state:
        st.session_state.circle_members = {
            "Stress Support Circle": ["Aarav", "Diya", "Raj"],
            "Productivity Boosters": ["Ishaan", "Tanya"],
            "Calm Minds": ["Riya", "Karan", "Ananya"]
        }

    st.markdown("### 🧠 AI Recommendation")
    user_feeling = st.text_area("💭 Describe how you feel today:", placeholder="e.g., I feel anxious about exams and deadlines...")

    if st.button("✨ Get Circle Recommendation"):
        if not user_feeling.strip():
            st.warning("Please share a few words about how you feel.")
        else:
            feeling_lower = user_feeling.lower()
            if any(word in feeling_lower for word in ["stress", "anxious", "pressure", "exam", "tired"]):
                rec_circle = "Stress Support Circle"
                reason = "It seems you're feeling academic or emotional stress. This group focuses on stress relief techniques 🌿."
            elif any(word in feeling_lower for word in ["focus", "lazy", "motivation", "discipline", "goal"]):
                rec_circle = "Productivity Boosters"
                reason = "You're looking to stay consistent and productive. This circle shares focus-building tips 💪."
            elif any(word in feeling_lower for word in ["peace", "relax", "calm", "meditation", "overthinking"]):
                rec_circle = "Calm Minds"
                reason = "You're seeking peace and balance — this group helps with mindfulness and relaxation 🌸."
            else:
                rec_circle = "Calm Minds"
                reason = "You seem in need of calm reflection — Calm Minds could be your safe space 🌿."

            st.success(f"💡 Recommended Circle: **{rec_circle}**")
            st.info(reason)

    st.markdown("---")
    st.markdown("### 🌼 Explore and Join Circles")

    circles = [
        {"name": "Stress Support Circle", "topic": "Managing academic and emotional stress"},
        {"name": "Productivity Boosters", "topic": "Staying focused, avoiding burnout"},
        {"name": "Calm Minds", "topic": "Mindfulness, relaxation, and balance"}
    ]

    for c in circles:
        members = st.session_state.circle_members.get(c["name"], [])
        with st.expander(f"{c['name']} ({len(members)} members)"):
            st.write(f"**Topic:** {c['topic']}")
            st.write("👥 **Members:** " + ", ".join(members))

            name = st.text_input(f"Enter your name to join {c['name']}:", key=f"name_{c['name']}")
            if st.button(f"Join {c['name']}", key=f"join_{c['name']}"):
                if not name.strip():
                    st.warning("Please enter your name before joining.")
                elif name in members:
                    st.info(f"✅ {name}, you’re already part of this circle!")
                else:
                    st.session_state.circle_members[c["name"]].append(name)
                    st.session_state.joined_circles[name] = c["name"]
                    st.success(f"🎉 Welcome {name}! You’ve joined **{c['name']}** 🌿")

    st.markdown("---")
    st.markdown("### 💫 Your Joined Circles")

    if st.session_state.joined_circles:
        user_names = list(st.session_state.joined_circles.keys())
        joined_groups = [st.session_state.joined_circles[n] for n in user_names]
        joined_df = pd.DataFrame({"Member": user_names, "Circle": joined_groups})
        st.dataframe(joined_df, use_container_width=True, height=150)
    else:
        st.info("You haven’t joined any circles yet. Join one to start connecting 💬")

    st.markdown("---")
    st.markdown("🌻 *Remember: you grow faster when you grow together.* 🌻")

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

# --- Emotion-Aware Wellness Tips ---
elif page == "Wellness Tips":
    st.header("💬 Emotion-Aware Wellness Assistant")
    st.write("✨ Express how you feel below — your app will understand your emotion and share a helpful wellness tip 🌿")

    st.markdown("""
        <style>
        .emotion-card {
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 1.2em;
            font-weight: 500;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
            margin-top: 20px;
            color: #333;
        }
        .happy { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
        .neutral { background: linear-gradient(135deg, #fff1eb 0%, #ace0f9 100%); }
        .sad { background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%); }
        </style>
    """, unsafe_allow_html=True)

    # User expresses emotion
    emotion_text = st.text_area("💭 Write how you feel today:", placeholder="e.g., I feel tired and anxious about my exams...")

    if st.button("💡 Get My Wellness Tip"):
        if not emotion_text.strip():
            st.warning("Please express your feelings first 💬")
        else:
            # Basic sentiment analysis (simple keyword-based)
            emotion_text_lower = emotion_text.lower()
            happy_words = ["happy", "great", "good", "excited", "joy", "grateful", "awesome"]
            sad_words = ["sad", "tired", "stressed", "depressed", "anxious", "upset", "angry", "lonely"]
            neutral_words = ["okay", "fine", "normal", "alright", "neutral"]

            mood = "neutral"
            if any(word in emotion_text_lower for word in happy_words):
                mood = "happy"
            elif any(word in emotion_text_lower for word in sad_words):
                mood = "sad"

            # Mood-based tips
            if mood == "happy":
                tips = [
                    "🌞 Keep this energy alive — share your joy with someone today!",
                    "💬 Write down 3 things that made you smile today — small joys matter.",
                    "🎵 Play your favorite upbeat song and celebrate yourself!",
                    "🌼 Use your positive energy to start something creative today!"
                ]
                selected_tip = tips[datetime.datetime.now().second % len(tips)]
                st.markdown(f"<div class='emotion-card happy'>😊 **You seem joyful!** <br><br>{selected_tip}</div>", unsafe_allow_html=True)

            elif mood == "sad":
                tips = [
                    "💖 It’s okay to rest — healing is progress too.",
                    "🌧️ Try writing down your feelings — you’ll feel lighter after.",
                    "🤍 Call a friend or listen to calming music — connection heals.",
                    "🌙 Breathe deeply and remind yourself: tough times pass, gentle soul."
                ]
                selected_tip = tips[datetime.datetime.now().second % len(tips)]
                st.markdown(f"<div class='emotion-card sad'>☁️ **You seem a bit low.** <br><br>{selected_tip}</div>", unsafe_allow_html=True)

            else:
                tips = [
                    "🌿 Take a short walk or stretch — clarity comes with motion.",
                    "☕ Make yourself a warm drink and take 5 mindful breaths.",
                    "📚 Read a quote or a short poem that inspires you.",
                    "🪷 Pause. Reflect. You’re doing just fine — one step at a time."
                ]
                selected_tip = tips[datetime.datetime.now().second % len(tips)]
                st.markdown(f"<div class='emotion-card neutral'>🌤️ **You seem calm.** <br><br>{selected_tip}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("✨ *Wellness begins with awareness — thank yourself for checking in today.* 🌸")


# --- Peer Support Circles (AI Recommendation + Interactive Join System) ---
elif page == "Peer Support Circles":
    st.header("🤝 Guided Peer Support Circles")
    st.markdown("✨ Join a circle that fits your current emotional needs or get an AI suggestion based on how you feel 💬")

    # Initialize circles and session data
    if "joined_circles" not in st.session_state:
        st.session_state.joined_circles = {}
    if "circle_members" not in st.session_state:
        st.session_state.circle_members = {
            "Stress Support Circle": ["Aarav", "Diya", "Raj"],
            "Productivity Boosters": ["Ishaan", "Tanya"],
            "Calm Minds": ["Riya", "Karan", "Ananya"]
        }

    st.markdown("### 🧠 AI Recommendation")
    user_feeling = st.text_area("💭 Describe how you feel today:", placeholder="e.g., I feel anxious about exams and deadlines...")

    if st.button("✨ Get Circle Recommendation"):
        if not user_feeling.strip():
            st.warning("Please share a few words about how you feel.")
        else:
            feeling_lower = user_feeling.lower()
            if any(word in feeling_lower for word in ["stress", "anxious", "pressure", "exam", "tired"]):
                rec_circle = "Stress Support Circle"
                reason = "It seems you're feeling academic or emotional stress. This group focuses on stress relief techniques 🌿."
            elif any(word in feeling_lower for word in ["focus", "lazy", "motivation", "discipline", "goal"]):
                rec_circle = "Productivity Boosters"
                reason = "You're looking to stay consistent and productive. This circle shares focus-building tips 💪."
            elif any(word in feeling_lower for word in ["peace", "relax", "calm", "meditation", "overthinking"]):
                rec_circle = "Calm Minds"
                reason = "You're seeking peace and balance — this group helps with mindfulness and relaxation 🌸."
            else:
                rec_circle = "Calm Minds"
                reason = "You seem in need of calm reflection — Calm Minds could be your safe space 🌿."

            st.success(f"💡 Recommended Circle: **{rec_circle}**")
            st.info(reason)

    st.markdown("---")
    st.markdown("### 🌼 Explore and Join Circles")

    circles = [
        {"name": "Stress Support Circle", "topic": "Managing academic and emotional stress"},
        {"name": "Productivity Boosters", "topic": "Staying focused, avoiding burnout"},
        {"name": "Calm Minds", "topic": "Mindfulness, relaxation, and balance"}
    ]

    for c in circles:
        members = st.session_state.circle_members.get(c["name"], [])
        with st.expander(f"{c['name']} ({len(members)} members)"):
            st.write(f"**Topic:** {c['topic']}")
            st.write("👥 **Members:** " + ", ".join(members))

            name = st.text_input(f"Enter your name to join {c['name']}:", key=f"name_{c['name']}")
            if st.button(f"Join {c['name']}", key=f"join_{c['name']}"):
                if not name.strip():
                    st.warning("Please enter your name before joining.")
                elif name in members:
                    st.info(f"✅ {name}, you’re already part of this circle!")
                else:
                    st.session_state.circle_members[c["name"]].append(name)
                    st.session_state.joined_circles[name] = c["name"]
                    st.success(f"🎉 Welcome {name}! You’ve joined **{c['name']}** 🌿")

    st.markdown("---")
    st.markdown("### 💫 Your Joined Circles")

    if st.session_state.joined_circles:
        user_names = list(st.session_state.joined_circles.keys())
        joined_groups = [st.session_state.joined_circles[n] for n in user_names]
        joined_df = pd.DataFrame({"Member": user_names, "Circle": joined_groups})
        st.dataframe(joined_df, use_container_width=True, height=150)
    else:
        st.info("You haven’t joined any circles yet. Join one to start connecting 💬")

    st.markdown("---")
    st.markdown("🌻 *Remember: you grow faster when you grow together.* 🌻")

# --- Personalized Stress Relief Plans (Smart Version) ---
elif page == "Stress Relief Plans":
    st.header("💖 Personalized Stress Relief Plans")
    st.write("🧘 Express your stress — get a custom relaxation plan that fits your situation and energy level 🌿")

    # Styling
    st.markdown("""
        <style>
        .plan-card {
            background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            color: #222;
            margin-top: 15px;
            font-size: 1.1em;
        }
        .plan-title {
            font-size: 1.4em;
            font-weight: bold;
            color: #2E8B57;
        }
        </style>
    """, unsafe_allow_html=True)

    # Input area
    user_stress = st.text_area("💭 What’s causing you stress today?", placeholder="e.g., I have too many assignments and can’t focus properly...")

    if st.button("🌸 Get My Stress Relief Plan"):
        if not user_stress.strip():
            st.warning("Please describe your stress to get a personalized plan.")
        else:
            stress_text = user_stress.lower()
            plan_title, plan_details, playlist = "", [], ""

            # --- AI-like pattern detection ---
            if any(word in stress_text for word in ["exam", "study", "assignment", "grades", "college", "school"]):
                plan_title = "🎓 Academic Pressure Plan"
                plan_details = [
                    "🧘 Take a 10-minute guided breathing break.",
                    "📅 Break your tasks into smaller steps — focus on one topic for 30 mins.",
                    "💧 Drink water and stretch for 2 minutes after every study hour.",
                    "🎧 Try a 'Focus & Calm' playlist to refresh your mind."
                ]
                playlist = "https://open.spotify.com/playlist/37i9dQZF1DX3PIPIT6lEg5"

            elif any(word in stress_text for word in ["work", "job", "office", "burnout", "deadline"]):
                plan_title = "💼 Workplace Burnout Plan"
                plan_details = [
                    "☕ Step away for a short mindful coffee or tea break.",
                    "📋 Write down 3 priorities — focus only on those today.",
                    "🌿 Go for a 5-minute walk outside or near a window.",
                    "🎧 Listen to an 'Anti-Stress Acoustic' playlist."
                ]
                playlist = "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0"

            elif any(word in stress_text for word in ["sleep", "insomnia", "tired", "fatigue"]):
                plan_title = "🌙 Sleep & Energy Recovery Plan"
                plan_details = [
                    "😴 Turn off screens 30 minutes before bed.",
                    "🧘 Try a short bedtime meditation (5-10 mins).",
                    "💤 Write one good thing about today before sleeping.",
                    "🎧 Play soft instrumental or ambient music."
                ]
                playlist = "https://open.spotify.com/playlist/37i9dQZF1DWZd79rJ6a7lp"

            elif any(word in stress_text for word in ["relationship", "friend", "family", "breakup", "alone", "lonely"]):
                plan_title = "💞 Emotional Healing Plan"
                plan_details = [
                    "💖 Talk to someone who understands — connection heals.",
                    "✍️ Write down your feelings — release what you can’t say out loud.",
                    "🌈 Watch or read something uplifting.",
                    "🪷 Do one self-care activity you love — music, art, or nature walk."
                ]
                playlist = "https://open.spotify.com/playlist/37i9dQZF1DX7gIoKXt0gmx"

            else:
                plan_title = "🌿 General Calm & Balance Plan"
                plan_details = [
                    "🪷 Breathe in deeply — count 4 in, 4 out — for 2 minutes.",
                    "💧 Drink a glass of water mindfully.",
                    "🧠 Note one small task you can finish easily.",
                    "🎵 Play something peaceful and look away from screens for 5 mins."
                ]
                playlist = "https://open.spotify.com/playlist/37i9dQZF1DWU0ScTcjJBdj"

            # --- Display result card ---
            st.markdown(f"<div class='plan-card'><div class='plan-title'>{plan_title}</div>", unsafe_allow_html=True)
            for step in plan_details:
                st.markdown(f"- {step}")
            st.markdown(f"</div>", unsafe_allow_html=True)
            st.markdown(f"🎧 [Open Recommended Playlist]({playlist})", unsafe_allow_html=True)

            st.success("💚 Remember — one small act of calm can change your entire day.")

    st.markdown("---")
    st.markdown("✨ *Your peace matters. Take one gentle step at a time.* 🌼")


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
