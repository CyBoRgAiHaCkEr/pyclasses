import streamlit as st
from groq import Groq

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Python Mentor", page_icon="🐍", layout="wide")

# Keeping the cool dark look but making it cleaner
st.markdown("""
    <style>
    .stApp { background-color: #0f1116; color: #e1e4e8; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stChatFloatingInputContainer { background-color: #0f1116; }
    [data-testid="stChatMessage"] { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- GROQ CONNECTION ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Please add your GROQ_API_KEY to Streamlit Secrets!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- THE "NORMAL" SYSTEM PROMPT ---
# This is what makes it speak like a regular person
NORMAL_PROMPT = """
You are a friendly, patient Python teacher. 
Speak naturally and simply, like you're chatting with a friend over coffee.
Avoid being overly "robotic" or "futuristic." 

Your Goal: 
1. Teach the basics of Python and Streamlit.
2. Explain how to put code on GitHub (calling it a place to save and share code).
3. Explain how to publish the app so others can see it.

Always be encouraging. If the user makes a mistake, say 'No worries, let's fix it' 
instead of 'System Error.' Use normal emojis like 😊, 🚀, and 👍.
"""

# --- SIDEBAR ---
with st.sidebar:
    st.title("👨‍🏫 Class Progress")
    st.write("Welcome! We're going to learn Python step-by-step.")
    st.divider()
    if st.button("Clear Conversation"):
        st.session_state.messages = [{"role": "system", "content": NORMAL_PROMPT}]
        st.rerun()

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": NORMAL_PROMPT}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything about Python..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Still using Llama 4 Scout for that 2026 speed
        stream = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            messages=st.session_state.messages,
            temperature=0.7, # Higher temperature makes it sound more human
            stream=True
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
