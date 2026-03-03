import streamlit as st
from groq import Groq

# --- HUD CONFIGURATION ---
st.set_page_config(page_title="NEURAL MENTOR v4.0", page_icon="🌐", layout="wide")

# Custom CSS for the Futuristic HUD Look
st.markdown("""
    <style>
    .stApp { background-color: #000814; color: #00f2ff; }
    [data-testid="stSidebar"] { background-color: #001d3d; border-right: 2px solid #00f2ff; }
    h1, h2, h3 { color: #00f2ff !important; text-shadow: 0 0 12px #00f2ff; font-family: 'Courier New', monospace; }
    .stChatFloatingInputContainer { background-color: #000814; }
    .stMarkdown { font-family: 'IBM Plex Mono', monospace; }
    /* Style for the chat bubbles */
    [data-testid="stChatMessage"] { background-color: #001d3d; border: 1px solid #00f2ff33; border-radius: 10px; }
    </style>
    """, unsafe_content_html=True)

# --- SYSTEM INITIALIZATION ---
try:
    # Set this in your Streamlit Cloud Secrets
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("❌ SYSTEM CRITICAL: GROQ_API_KEY NOT DETECTED. PLEASE ADD TO SECRETS.")
    st.stop()
    st.baloons()

# --- THE MENTOR INTELLIGENCE (System Prompt) ---
SYSTEM_PROMPT = """
You are 'NEURAL MENTOR', an advanced AI teaching Python to absolute beginners.
YOUR MISSION: Guide them to build a Streamlit app and push it to GitHub.

OPERATIONAL PROTOCOLS:
1. BASICS FIRST: Explain variables as 'Data Cells' and functions as 'Sub-routines'.
2. GITHUB UPLINK: Explain GitHub as a 'Galactic Archive' where code is safe.
3. STREAMLIT COMMANDS: Teach st.title, st.write, and st.button as 'HUD Widgets'.
4. DEPLOYMENT: Always mention 'requirements.txt' is the 'Manifest' the cloud needs.
5. STYLE: Be encouraging, techy, and use emojis like 🌐, 🚀, and 🐍.
"""

# --- HUD SIDEBAR ---
with st.sidebar:
    st.title("📡 HUD STATUS")
    st.write("---")
    st.write("**CORE:** Llama 4 Scout")
    st.write("**ENGINE:** Groq LPU™")
    st.write("**LATENCY:** < 10ms")
    st.write("---")
    st.subheader("🛠 UPLINK MANIFEST")
    st.code("1. streamlit_app.py\n2. requirements.txt\n3. README.md", language="text")
    st.success("SCAN COMPLETE: READY TO TEACH")

# --- CHAT INTERFACE ---
st.title("🌐 NEURAL MENTOR // PYTHON CORE")
st.caption("Initializing Learning Module: GitHub & Streamlit Basics...")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Display Neural Feed (Chat History)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input (Neural Command)
if prompt := st.chat_input("Input command (e.g., 'How do I start?')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Llama 4 Scout 17B-16E: Mixture of Experts at 750+ t/s
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            messages=st.session_state.messages,
            temperature=0.4,
            stream=True
        )
        response = st.write_stream(completion)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
