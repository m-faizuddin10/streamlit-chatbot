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
        /* Main app background */
        .stApp {
            background: #e3f2fd !important; /* sky blue */
            color: #111111 !important;
        }
        /* Sidebar background and text */
        section[data-testid="stSidebar"] {
            background-color: #bbdefb !important; /* lighter sky blue */
            color: #111111 !important;
        }
        /* Sidebar header and text */
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6, .stSidebar p, .stSidebar label {
            color: #111111 !important;
        }
        /* All containers and blocks */
        .stContainer, .stMarkdown, .stTextInput, .stSelectbox, .stCheckbox, .stButton, .stChatMessage {
            background-color: #e3f2fd !important; /* sky blue */
            color: #111111 !important;
        }
        /* Chat message bubbles */
        .stChatMessage.user {
            background-color: #90caf9 !important; /* medium sky blue */
            color: #111111 !important;
            border-radius: 12px;
            padding: 8px;
        }
        .stChatMessage.assistant {
            background-color: #bbdefb !important; /* lighter sky blue */
            color: #111111 !important;
            border-radius: 12px;
            padding: 8px;
        }
        /* Title */
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #111111;
        }
        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #222222;
            margin-bottom: 30px;
        }
        /* Buttons (main and sidebar) */
        .stButton > button, section[data-testid="stSidebar"] .stButton > button {
            border-radius: 10px;
            background-color: #90caf9 !important; /* medium sky blue */
            color: #111111 !important;
            font-weight: bold;
            border: 1px solid #64b5f6;
            box-shadow: none !important;
        }
        /* Input box */
        .stTextInput>div>div>input {
            background-color: #e3f2fd !important;
            color: #111111 !important;
        }
        /* Selectbox */
        .stSelectbox>div>div>div {
            background-color: #e3f2fd !important;
            color: #111111 !important;
        }
        /* Checkbox */
        .stCheckbox>div {
            background-color: #e3f2fd !important;
            color: #111111 !important;
        }
        /* Code block styling */
        pre, code {
            background-color: #ffffff !important;
            color: #111111 !important;
            border-radius: 8px;
            padding: 12px;
            font-size: 15px;
            font-family: 'Fira Mono', 'Consolas', 'Monaco', monospace;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
            margin-bottom: 10px;
            display: block;
        }
        /* Remove box shadows for a flat look */
        .stButton > button, .stTextInput>div>div>input, .stSelectbox>div>div>div, .stCheckbox>div {
            box-shadow: none !important;
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

# Model selection (only supported models)
model_choice = st.sidebar.selectbox(
    "Choose AI Model:",
    [
        "llama-3.1-8b-instant",       # ✅ Fast, cheaper
        "llama-3.1-70b-versatile",    # ✅ More capable, larger
        "gemma2-9b-it"                # ✅ Google Gemma-2 fine-tuned
    ],
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
        st.markdown(
            f"<span style='color:#111111'>{message['content']}</span>",
            unsafe_allow_html=True
        )

# ----------------- CHAT INPUT -----------------
if prompt := st.chat_input("💬 Type your message here..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user bubble
    with st.chat_message("user"):
        st.markdown(
            f"<span style='color:#111111'>{prompt}</span>",
            unsafe_allow_html=True
        )

    # Assistant reply
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
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
                    message_placeholder.markdown(
                        f"<span style='color:#111111'>{full_response}▌</span>",
                        unsafe_allow_html=True
                    )
                message_placeholder.markdown(
                    f"<span style='color:#111111'>{full_response}</span>",
                    unsafe_allow_html=True
                )
            else:
                # Non-stream response
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=st.session_state.messages,
                )
                full_response = response.choices[0].message.content
                message_placeholder.markdown(
                    f"<span style='color:#111111'>{full_response}</span>",
                    unsafe_allow_html=True
                )

        except Exception as e:
            # fallback in case of model issues
            full_response = f"⚠️ Error with model `{model_choice}`. Falling back to llama-3.1-8b-instant.\n\nError: {str(e)}"
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                )
                full_response = response.choices[0].message.content
            except Exception as inner_e:
                full_response = f"❌ Could not generate a response. Error: {inner_e}"

            message_placeholder.markdown(
                f"<span style='color:#111111'>{full_response}</span>",
                unsafe_allow_html=True
            )

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})





        

