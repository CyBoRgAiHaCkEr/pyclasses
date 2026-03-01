import streamlit as st
import paho.mqtt.client as mqtt
import base64
from io import BytesIO
from PIL import Image
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="Global Chat App", page_icon="💬")

# --- INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "connected" not in st.session_state:
    st.session_state.connected = False
if "client" not in st.session_state:
    st.session_state.client = None

# --- SIDEBAR: CONFIGURATION ---
st.sidebar.title("⚙️ Chat Setup")
st.sidebar.write("Ensure you and your friend use the **same** Secret Channel but **swap** names!")

secret_channel = st.sidebar.text_input("Secret Channel", value="my_super_secret_room_99")
my_name = st.sidebar.text_input("My Name", value="User1")
friend_name = st.sidebar.text_input("Friend's Name", value="User2")

# Define routing topics based on the sidebar inputs
MY_TEXT_TOPIC = f"{secret_channel}/{my_name}/text"
MY_IMAGE_TOPIC = f"{secret_channel}/{my_name}/image"
FRIEND_TEXT_TOPIC = f"{secret_channel}/{friend_name}/text"
FRIEND_IMAGE_TOPIC = f"{secret_channel}/{friend_name}/image"

# --- NETWORK FUNCTIONS ---
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        client.subscribe(FRIEND_TEXT_TOPIC)
        client.subscribe(FRIEND_IMAGE_TOPIC)

def on_message(client, userdata, msg):
    # Save incoming messages to the Streamlit session state
    if msg.topic == FRIEND_TEXT_TOPIC:
        st.session_state.messages.append({"sender": friend_name, "type": "text", "content": msg.payload.decode()})
    elif msg.topic == FRIEND_IMAGE_TOPIC:
        st.session_state.messages.append({"sender": friend_name, "type": "image", "content": msg.payload})

# --- CONNECT / DISCONNECT BUTTONS ---
if not st.session_state.connected:
    if st.sidebar.button("🟢 Connect to Chat"):
        # Setup MQTT using WebSockets to bypass firewalls
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport="websockets")
        client.on_connect = on_connect
        client.on_message = on_message
        
        client.connect("broker.hivemq.com", 8000, 60)
        client.loop_start() # Run in background
        
        st.session_state.client = client
        st.session_state.connected = True
        st.rerun()
else:
    st.sidebar.success("✅ Connected!")
    if st.sidebar.button("🔴 Disconnect"):
        st.session_state.client.loop_stop()
        st.session_state.client.disconnect()
        st.session_state.connected = False
        st.session_state.client = None
        st.rerun()

# --- MAIN UI ---
st.title(f"Chatting with {friend_name}")

# Refresh button to check for background messages
if st.button("🔄 Check for New Messages"):
    st.rerun()

st.divider()

# Display Chat History
for msg in st.session_state.messages:
    # Render user messages on one side, friend messages on the other
    with st.chat_message("user" if msg["sender"] == my_name else "assistant"):
        st.markdown(f"**{msg['sender']}**")
        
        if msg["type"] == "text":
            st.write(msg["content"])
            
        elif msg["type"] == "image":
            try:
                # Decode image and display it
                img_bytes = base64.b64decode(msg["content"])
                image = Image.open(BytesIO(img_bytes))
                st.image(image, use_container_width=True)
            except Exception:
                st.error("Failed to load image.")

# --- INPUT AREAS ---
if st.session_state.connected:
    # 1. Text Input 
    prompt = st.chat_input("Type a message...")
    if prompt:
        # Add to local history and send
        st.session_state.messages.append({"sender": my_name, "type": "text", "content": prompt})
        st.session_state.client.publish(MY_TEXT_TOPIC, prompt)
        st.rerun()

    # 2. Image Upload
    with st.expander("📷 Send a Photo"):
        uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
        if st.button("Send Image") and uploaded_file is not None:
            # Convert file to text and send
            file_bytes = uploaded_file.getvalue()
            encoded_string = base64.b64encode(file_bytes)
            
            st.session_state.messages.append({"sender": my_name, "type": "image", "content": encoded_string})
            st.session_state.client.publish(MY_IMAGE_TOPIC, encoded_string)
            
            st.success("✅ Image sent!")
            time.sleep(1) # Brief pause so the success message is visible
            st.rerun()
else:
    st.info("👈 Set your names and click 'Connect to Chat' in the sidebar to start!")
