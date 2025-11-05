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


# --- 🌿 AI-Powered Stress Relief Plans 2.0 ---
elif page == "Stress Relief Plans":
    st.header("💖 AI-Powered Stress Relief Companion")
    st.markdown("#### Tell me what’s troubling you — I’ll help you calm your mind with a custom recovery plan 🌸")

    # 🎨 Calming UI
    st.markdown("""
        <style>
        .relief-card {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            margin-top: 20px;
            color: #333;
        }
        .step-box {
            background: rgba(255, 255, 255, 0.6);
            border-left: 6px solid #5cb85c;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .affirmation {
            background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: 500;
            color: #2c3e50;
            margin-top: 20px;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    # 🧘 User Input
    user_text = st.text_area("💭 What’s been stressing you out lately?", 
                             placeholder="e.g., I’m so tired from constant deadlines and can’t focus anymore...")

    if st.button("🌿 Generate My Recovery Plan"):
        if not user_text.strip():
            st.warning("Please describe your situation or emotion 💬")
        else:
            text = user_text.lower()
            mood = "neutral"
            plan, affirmation, link = [], "", ""

            # --- AI Emotion Detection & Plan Creation ---
            if any(word in text for word in ["exam", "assignment", "study", "grades", "school", "college"]):
                mood = "academic stress"
                title = "📚 Academic Overload"
                plan = [
                    "🎧 Play a soft instrumental playlist while studying — background calm boosts focus.",
                    "📅 Break study blocks into 30-minute sprints and reward yourself after each one.",
                    "💧 Take short water & stretch breaks — physical reset improves memory retention.",
                    "🧘 Try deep breathing for 3 minutes before revising difficult topics.",
                    "🌼 End the day by journaling one positive learning you achieved today."
                ]
                link = "https://open.spotify.com/playlist/37i9dQZF1DX3PIPIT6lEg5"
                affirmation = "You are learning at your own pace — and that’s perfectly okay 🌿"

            elif any(word in text for word in ["work", "office", "boss", "job", "project", "meeting", "deadline"]):
                mood = "work stress"
                title = "💼 Workplace Burnout"
                plan = [
                    "☕ Step away from your desk and take 10 deep breaths by the window.",
                    "🗂️ Write down only 3 essential tasks for today — small wins matter.",
                    "📞 Speak kindly to yourself — pressure does not define worth.",
                    "🌙 When you log off, truly disconnect — go for a short walk outside.",
                    "🎧 Listen to a relaxation playlist during your commute or break."
                ]
                link = "https://open.spotify.com/playlist/37i9dQZF1DX83CujKHHOn"
                affirmation = "You deserve peace — your value is not measured by productivity 💼"

            elif any(word in text for word in ["family", "relationship", "friend", "breakup", "alone", "lonely"]):
                mood = "emotional stress"
                title = "💖 Emotional Healing"
                plan = [
                    "💌 Write down your feelings — release what hurts onto paper.",
                    "📞 Call or text someone you trust — connection soothes pain.",
                    "🕯️ Light a candle or play calming music; let your space feel safe again.",
                    "🌙 Do one act of self-kindness — even resting counts.",
                    "🙏 Remind yourself that your emotions are valid and temporary."
                ]
                link = "https://open.spotify.com/playlist/37i9dQZF1DWZd79rJ6a7lp"
                affirmation = "Your heart is strong — even in silence, you are healing 🤍"

            elif any(word in text for word in ["tired", "sleep", "fatigue", "insomnia", "restless"]):
                mood = "fatigue"
                title = "😴 Exhaustion & Sleep Fatigue"
                plan = [
                    "🛏️ Unplug from screens for 30 minutes before bed — light resets your mind.",
                    "🧘 Try 4-7-8 breathing — inhale for 4, hold for 7, exhale for 8.",
                    "💧 Drink warm water or herbal tea — calm your body from within.",
                    "🎵 Play slow ambient music or rain sounds before sleeping.",
                    "🌼 Tomorrow is a new start — rest is your reset button."
                ]
                link = "https://www.youtube.com/watch?v=ZToicYcHIOU"
                affirmation = "You are allowed to pause — rest is not weakness, it’s self-respect 🌙"

            elif any(word in text for word in ["panic", "anxiety", "overthinking", "fear", "nervous"]):
                mood = "anxiety"
                title = "🌬️ Anxiety & Overthinking"
                plan = [
                    "🫁 Focus on your breath — name 3 things you can see, 2 you can hear, 1 you can feel.",
                    "🕊️ Repeat softly: ‘I am safe right now.’",
                    "✍️ Write down your anxious thoughts, then fold the paper — your mind will follow.",
                    "💧 Drink cool water and place a hand on your chest while breathing slowly.",
                    "🎧 Listen to soft lo-fi or rain sounds for 5 minutes — sensory calm works wonders."
                ]
                link = "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0"
                affirmation = "You are safe. You are grounded. You are more than your thoughts 🌬️"

            else:
                mood = "general stress"
                title = "🌿 Gentle Mind Reset"
                plan = [
                    "🪷 Sit comfortably and take 5 mindful breaths — let your shoulders drop.",
                    "☀️ Step into sunlight for 2 minutes — nature restores balance.",
                    "📖 Read one positive paragraph or quote that uplifts your spirit.",
                    "🍵 Have a warm drink and do nothing — yes, absolutely nothing — for 3 minutes.",
                    "💌 Whisper to yourself: ‘I’m doing enough, I am enough.’"
                ]
                link = "https://open.spotify.com/playlist/37i9dQZF1DWZd79rJ6a7lp"
                affirmation = "Even doing nothing for a while is an act of healing 🌼"

            # --- 🌸 Display the AI-generated plan ---
            st.markdown(f"<div class='relief-card'><h3>{title}</h3>", unsafe_allow_html=True)
            for i, step in enumerate(plan, start=1):
                st.markdown(f"<div class='step-box'><b>Step {i}:</b> {step}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"🎧 [Click here for a recommended playlist to calm your mind]({link})", unsafe_allow_html=True)
            st.markdown(f"<div class='affirmation'>{affirmation}</div>", unsafe_allow_html=True)


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
