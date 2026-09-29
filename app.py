import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash-lite"

st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="✨",
    layout="centered"
)

# ---------------------- CUSTOM CSS ----------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    /* ---------- Background ---------- */
    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(124, 58, 237, 0.35), transparent 40%),
            radial-gradient(circle at 85% 15%, rgba(6, 182, 212, 0.30), transparent 40%),
            radial-gradient(circle at 50% 90%, rgba(236, 72, 153, 0.28), transparent 45%),
            #0b0b1a;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
        color: #e8e8f5;
    }

    /* Clean up default Streamlit chrome (keep sidebar toggle working) */
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    /* ---------- Main container ---------- */
    .block-container {
        max-width: 820px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    /* ---------- Title ---------- */
    h1 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.6rem !important;
        font-weight: 700 !important;
        text-align: center;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #a78bfa, #22d3ee, #f472b6, #a78bfa);
        background-size: 300% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 6s linear infinite;
        padding-bottom: 0;
    }
    @keyframes shine { to { background-position: 300% 0; } }

    .subtitle {
        text-align: center;
        color: #b9b9d6;
        font-size: 0.95rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-weight: 300;
        margin-bottom: 1.5rem;
    }

    /* ---------- Welcome card (empty chat) ---------- */
    .welcome {
        text-align: center;
        margin: 2.5rem auto;
        padding: 2.2rem 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
        animation: floatIn 0.8s ease both;
    }
    .welcome .big { font-size: 3rem; }
    .welcome h3 { color: #f1f1ff; margin: 0.4rem 0; font-weight: 600; }
    .welcome p { color: #a9a9c9; margin: 0; }

    @keyframes floatIn {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ---------- Chat bubbles ---------- */
    div[data-testid="stChatMessage"] {
        padding: 1rem 1.2rem;
        margin-bottom: 0.9rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.10);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.30);
        animation: floatIn 0.5s ease both;
        max-width: 88%;
    }

    /* Assistant bubble (default) - left */
    div[data-testid="stChatMessage"] {
        background: linear-gradient(145deg, rgba(124, 58, 237, 0.16), rgba(6, 182, 212, 0.10));
        border-left: 4px solid #22d3ee;
        margin-right: auto;
    }

    /* User bubble - right */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.30), rgba(124, 58, 237, 0.30));
        border-left: 1px solid rgba(255, 255, 255, 0.10);
        border-right: 4px solid #f472b6;
        margin-left: auto;
        margin-right: 0;
        flex-direction: row-reverse;
        text-align: right;
    }

    /* Bubble text */
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li {
        color: #efeffc !important;
        line-height: 1.75;
        font-size: 1rem;
    }
    div[data-testid="stChatMessage"] code {
        background: rgba(0, 0, 0, 0.45);
        color: #67e8f9;
        border-radius: 6px;
        padding: 2px 6px;
    }
    div[data-testid="stChatMessage"] pre {
        background: rgba(5, 5, 20, 0.85) !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.10);
        text-align: left;
    }

    /* Avatars */
    div[data-testid="stChatMessage"] [data-testid^="stChatMessageAvatar"] {
        background: linear-gradient(135deg, #7c3aed, #06b6d4);
        border-radius: 50%;
        box-shadow: 0 0 18px rgba(124, 58, 237, 0.55);
    }

    /* ---------- Chat input (bottom bar) ---------- */
    div[data-testid="stBottom"],
    div[data-testid="stBottom"] > div {
        background: transparent !important;
    }
    div[data-testid="stChatInput"] {
        background: rgba(15, 15, 40, 0.75) !important;
        border: 1.5px solid rgba(167, 139, 250, 0.40) !important;
        border-radius: 22px !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.45);
        transition: all 0.3s ease;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #22d3ee !important;
        box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.18),
                    0 0 28px rgba(167, 139, 250, 0.40);
    }
    div[data-testid="stChatInput"] textarea {
        color: #f1f1ff !important;
        font-family: 'Poppins', sans-serif;
        background: transparent !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #7f7fa6 !important;
        font-style: italic;
    }
    div[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #7c3aed, #06b6d4, #ec4899) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        transition: transform 0.2s ease;
    }
    div[data-testid="stChatInput"] button:hover {
        transform: scale(1.1);
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: rgba(10, 10, 28, 0.85);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px);
    }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #d8d8f0 !important;
    }
    .side-stat {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 14px;
        padding: 0.8rem 1rem;
        margin-top: 0.8rem;
        color: #cfcfee;
        font-size: 0.9rem;
    }

    /* ---------- Buttons ---------- */
    .stButton > button, .stDownloadButton > button {
        width: 100%;
        padding: 0.7rem 1.2rem;
        border: none;
        border-radius: 14px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #ffffff;
        background: linear-gradient(135deg, #7c3aed, #06b6d4, #ec4899);
        background-size: 250% 250%;
        animation: gradientMove 6s ease infinite;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.40);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    @keyframes gradientMove {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 14px 34px rgba(6, 182, 212, 0.45);
        color: #ffffff;
        border: none;
    }

    /* ---------- Alerts / spinner ---------- */
    div[data-testid="stAlert"] {
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    div[data-testid="stAlert"] p { color: #f0f0ff !important; }
    div[data-testid="stSpinner"] p { color: #22d3ee !important; }

    /* ---------- Scrollbar ---------- */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #0b0b1a; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#7c3aed, #06b6d4);
        border-radius: 10px;
    }

    /* ---------- Mobile ---------- */
    @media (max-width: 640px) {
        h1 { font-size: 1.9rem !important; }
        div[data-testid="stChatMessage"] { max-width: 100%; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- SESSION STATE ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": "user" | "assistant", "content": str}

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.markdown("## ✨ Chat Controls")
    if st.button("🗑️ New chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        f"<div class='side-stat'>💬 Messages in this chat: "
        f"<b>{len(st.session_state.messages)}</b></div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div class='side-stat'>🤖 Model: <b>{MODEL_NAME}</b></div>",
        unsafe_allow_html=True
    )

# ---------------------- HEADER ----------------------
st.title("✨ GEMINI AI CHATBOT")
st.markdown("<div class='subtitle'>Ask Gemini anything</div>", unsafe_allow_html=True)

# ---------------------- HELPERS ----------------------
def build_contents(messages):
    """Convert chat history into the format Gemini expects."""
    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})
    return contents


def stream_reply(messages):
    """Yield the response text piece by piece for a typing effect."""
    stream = client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=build_contents(messages)
    )
    for chunk in stream:
        if chunk.text:
            yield chunk.text


# ---------------------- SHOW HISTORY ----------------------
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome">
            <div class="big">🚀</div>
            <h3>Hello! How can I help you today?</h3>
            <p>Type a message below to start chatting with Gemini.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------------------- CHAT INPUT ----------------------
user_input = st.chat_input("Message Gemini...")

if user_input:
    # Show and save the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # Get and stream Gemini's reply
    with st.chat_message("assistant", avatar="✨"):
        try:
            reply = st.write_stream(stream_reply(st.session_state.messages))
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            # Remove the unanswered user message so the history stays valid
            st.session_state.messages.pop()