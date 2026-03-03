import streamlit as st
from groq import Groq

# 1. Page Setup
st.set_page_config(page_title="Python Teacher", page_icon="👨‍🏫")
st.title("👨‍🏫 Your Python Mentor")

# 2. Check for API Key
if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing API Key! Please add GROQ_API_KEY to your Streamlit Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. Simple Human Personality
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a normal, friendly human teacher. Speak simply. No robot talk. Help the user learn Python, GitHub, and Streamlit step-by-step."}
    ]

# 4. Display Chat History
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# 5. The Chat Logic
if prompt := st.chat_input("Hi! What do you want to learn first?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
         st.balloons()

    with st.chat_message("assistant"):
        placeholder = st.empty() # Create a blank spot on the page
        full_response = ""
        
        # Start the stream
        stream = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=st.session_state.messages,
            stream=True
        )

        # MANUALLY grab the text from the JSON chunks
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                text_chunk = chunk.choices[0].delta.content
                full_response += text_chunk
                placeholder.markdown(full_response + "▌") # Update the spot with new text
        
        placeholder.markdown(full_response) # Final update without the cursor
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

