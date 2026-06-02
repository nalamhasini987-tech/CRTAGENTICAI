import os
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from utils.chat_storage import save_chat

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

genai.configure(api_key=api_key)

# -------------------------------
# Gemini Model
# -------------------------------
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------
# Load Campus Data
# -------------------------------
try:
    with open("campus_data.txt", "r", encoding="utf-8") as file:
        campus_data = file.read()
except:
    campus_data = "Campus information unavailable."

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Vignan Campus Companion",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("🎓 Campus Companion")

st.sidebar.markdown("---")

st.sidebar.write("Agentic AI Project")

st.sidebar.write("Developed Using:")
st.sidebar.write("✅ Gemini AI")
st.sidebar.write("✅ Streamlit")
st.sidebar.write("✅ Multi-Agent Logic")

st.sidebar.markdown("---")

st.sidebar.write("Available Agents")
st.sidebar.write("🧭 Navigation Agent")
st.sidebar.write("📚 FAQ Agent")
st.sidebar.write("🎉 Event Agent")
st.sidebar.write("🏫 Campus Information Agent")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "AI Assistant",
        "Campus Map"
    ]
)

# -------------------------------
# Chat History
# -------------------------------
st.sidebar.markdown("---")

if st.sidebar.button("📜 Show Chat History"):

    try:
        with open("data/chat_history.json", "r") as file:
            chats = json.load(file)

        st.write("Chats Found:", len(chats))
        st.sidebar.subheader("📜 Previous Conversations")

        if len(chats) == 0:
            st.info("No conversations yet.")

        else:
            for chat in reversed(chats):

                st.sidebar.write("👤", chat["user"])
                st.sidebar.write("🤖", chat["assistant"])
                st.sidebar.markdown("---")

                

    except:
        st.info("No chat history found.")

# =====================================================
# AI ASSISTANT PAGE
# =====================================================

if page == "AI Assistant":

    st.title("🎓 Vignan Campus Companion")

    st.markdown(
        "### Your Smart AI Campus Assistant"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Departments", "12")

    with col2:
        st.metric("Facilities", "20+")

    with col3:
        st.metric("Student Clubs", "5+")

    with col4:
        st.metric("Events", "10+")

    st.info(
        "Ask questions about departments, library, hostel, events, transport, offices and campus facilities."
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success("🧭 Navigation")

    with col2:
        st.success("📚 FAQ")

    with col3:
        st.success("🎉 Events")

    with col4:
        st.success("🏫 Information")

    st.markdown("---")

    question = st.text_input(
        "Ask your question:",
        placeholder="Example: Where is the Examination Branch?"
    )

    if st.button("Ask"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:
            # Show campus map directly if user asks for map
            if "map" in question.lower():

                st.subheader("🗺️ Vignan Campus Map")

                st.image(
                    "assets/campus_map.jpeg",
                    width=500
                )

                st.success("Vignan University Campus Map")

                st.stop()
            greetings = [
                "hi",
                "hello",
                "good morning",
                "good afternoon",
                "good evening"
            ]

            if question.lower() in greetings:

                response_text = (
                    "Hello! Welcome to Vignan Campus Companion. "
                    "How can I assist you today regarding campus facilities, "
                    "departments, events, hostel, library, placements, "
                    "or student services?"
                )

                st.success(response_text)

            else:

                # Agent Selection Logic
                if any(word in question.lower() for word in
                       ["where", "location", "reach", "find"]):

                    agent_name = "🧭 Navigation Agent"

                elif any(word in question.lower() for word in
                         ["event", "mahotsav", "workshop", "club"]):

                    agent_name = "🎉 Event Agent"

                elif any(word in question.lower() for word in
                         ["fee", "hostel", "library", "transport"]):

                    agent_name = "📚 FAQ Agent"

                else:

                    agent_name = "🏫 Campus Information Agent"

                prompt = f"""
You are acting as the {agent_name}.

Use ONLY the following campus information to answer.

Campus Information:
{campus_data}

Student Question:
{question}

Provide a clear, helpful and student-friendly answer.
"""

                with st.spinner("🤖 AI Agent is thinking..."):

                    response = model.generate_content(prompt)

                response_text = response.text

                save_chat(
                    question,
                    response_text
                )

                st.subheader("🤖 Selected Agent")
                st.success(agent_name)

                st.subheader("📌 Answer")

                st.markdown(
                    f"""
                    <div style="
                        background-color:#f0f2f6;
                        padding:20px;
                        border-radius:10px;
                        color:black;
                    ">
                    {response_text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# =====================================================
# CAMPUS MAP PAGE
# =====================================================

elif page == "Campus Map":

    st.title("🗺️ Vignan Campus Navigation")

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.image(
            "assets/campus_map.jpeg",
            width=350
        )

    st.markdown("### 📍 Select Destination")

    destination = st.selectbox(
        "Choose Destination",
        [
            "Library",
            "N Block",
            "U Block",
            "Girls Hostel",
            "Boys Hostel",
            "Convocation Hall",
            "Canteen"
        ]
    )

    routes = {
        "Library": "📚 Library is located beside A Block.",
        "N Block": "🏫 CSE and ACSE Departments are located in N Block.",
        "U Block": "🏫 IT, MBA, MCA, Civil and Mechanical Departments are in U Block.",
        "Girls Hostel": "🏨 Girls Hostel is located near the pond area.",
        "Boys Hostel": "🏨 Boys Hostel is located beside Pharmacy College.",
        "Convocation Hall": "🎤 Convocation Hall is near U Block.",
        "Canteen": "🍽️ Canteen is located near N Block."
    }

    st.success(routes[destination])

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")

st.caption(
    "Campus Companion Agent | Agentic AI Project | Powered by Gemini AI"
)