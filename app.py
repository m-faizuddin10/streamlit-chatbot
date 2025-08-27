import streamlit as st
from groq import Groq

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="TechVerse AI",
    page_icon="🤖",
    layout="wide"
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
    <style>
        /* App background */
        .stApp {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #F5F5F5;
        }
        /* Title */
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #00E5FF;
        }
        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #B0BEC5;
            margin-bottom: 30px;
        }
        /* Chat message bubbles */
        .stChatMessage.user {
            background-color: #1E88E5 !important;
            color: white !important;
            border-radius: 12px;
            padding: 8px;
        }
        .stChatMessage.assistant {
            background-color: #263238 !important;
            color: #ECEFF1 !important;
            border-radius: 12px;
            padding: 8px;
        }
        /* Sidebar styling */
        .css-1d391kg, .css-18ni7ap {
            background-color: #1C1C1C !important;
        }
        /* Buttons */
        .stButton > button {
            border-radius: 10px;
            background-color: #FF5252;
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- HEADER -----------------
st.markdown("<div class='title'>🤖 TechVerse AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your smart assistant powered by Groq AI</div>", unsafe_allow_html=True)

# ----------------- INIT CLIENT -----------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------- SIDEBAR -----------------
st.sidebar.header("⚙️ Settings")

# Model selection
model_choice = st.sidebar.selectbox(
    "Choose AI Model:",
    ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
    index=0
)

# Streaming or not
use_stream = st.sidebar.checkbox("Enable Streaming", value=True)

# Clear history
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []

# ----------------- SESSION STATE -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcome assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hi! I'm **Faiz**, your AI companion. How can I help you?"
    })

# ----------------- DISPLAY CHAT HISTORY -----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------- CHAT INPUT -----------------
if prompt := st.chat_input("💬 Type your message here..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user bubble
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant reply
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        if use_stream:
            # Streamed response
            stream = client.chat.completions.create(
                model=model_choice,
                messages=st.session_state.messages,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        else:
            # Non-stream response
            response = client.chat.completions.create(
                model=model_choice,
                messages=st.session_state.messages,
            )
            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})




        

