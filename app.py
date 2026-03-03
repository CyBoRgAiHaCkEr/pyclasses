import streamlit as st
from groq import Groq

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Python Coach", page_icon="🐍", layout="wide")

# --- INITIALIZE GROQ ---
# You will set this key in Streamlit Cloud "Secrets"
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing GROQ_API_KEY! Add it to your Streamlit Secrets.")
    st.stop()

# --- SYSTEM PROMPT (The "Teacher" Personality) ---
SYSTEM_PROMPT = """
You are a friendly 'Basics-First' Python Mentor.The User Is Mayu. 
Your goal: Teach a beginner how to write Python code in Streamlit and publish it to GitHub.
Rules:
1. Use simple analogies (Variables = Boxes, Functions = Recipes).
2. Do not give the whole answer at once. Ask the student to try one line of code first.
3. Explain that GitHub is a 'Cloud Save' for code.
4. Explain that Streamlit turns code into a Website.
5. If they are ready to publish, tell them they MUST have a 'requirements.txt' file.
"""

# --- SIDEBAR: PROGRESS TRACKER ---
with st.sidebar:
    st.title("🎓 Learning Path")
    step = st.radio("Current Lesson:", 
                    ["1. Python Basics", "2. Streamlit UI", "3. GitHub & Deployment"])
    
    st.divider()
    st.info("Tip: Always test your code locally before pushing to GitHub!")

# --- CHAT INTERFACE ---
st.title("🐍 Your AI Python Mentor")
st.caption("Powered by Groq | Meta Llama 4 Scout")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask me a basic Python question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Calling Groq for the Llama 4 Scout model
        completion = client.chat.completions.create(
            model="llama3-70b-8192", # Update to "llama-4-scout-17b" when live in your region
            messages=st.session_state.messages,
            temperature=0.6,
            stream=True
        )
        response = st.write_stream(completion)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
