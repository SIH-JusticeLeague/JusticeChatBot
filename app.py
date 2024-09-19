import streamlit as st
from main import *
from main import output

chatbot_response = output

def chatbot_response(user_input):
    if 'hello' in user_input.lower():
        return "Hello! How can I assist you today?"
    else:
        return "I'm just a simple chatbot, but I'm learning more every day!"

# Streamlit app UI
st.title("NYAY-SAHAY")

st.markdown("### How can I assist you today?")

# Initialize session state if not already done
if "history" not in st.session_state:
    st.session_state.history = []

# Create the input field and submit button (we will hide the submit button using CSS)
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("You:", key="input_area_unique")
    submit_button = st.form_submit_button(label='Send') 

# Handle input submission when the user presses Enter
if submit_button and user_input:
    response = chatbot_response(user_input)
    st.session_state.history.append({
        "user": user_input,
        "bot": response
    })

# Handle reset button
if st.button('Reset'):
    st.session_state.history = []

# Display chat history with each message in a new row
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        
    }
    .chat-message.user {
        background-color: #2e2e2e;
        padding: 10px;
        border-radius: 10px;
        color: white;
        text-align: right; 
        word-wrap: break-word;
        margin-bottom: 10px;
    }
    .chat-message.bot {
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 10px;
        color: white;
        text-align: left; 
        word-wrap: break-word;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for message in reversed(st.session_state.history):
    st.markdown(f"""
    <div class="chat-message bot">
        <b>Bot</b>:<br> {message["bot"]}
    </div>
    <div class="chat-message user">
        <b>You</b>:<br> {message["user"]}
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Custom CSS for styling the input and word wrapping
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: white;
        word-wrap: break-word;
        white-space: pre-wrap;  /* Ensures word wrapping for long inputs */
    }
    /* Hide the submit button */
    button[kind="secondaryFormSubmit"] {
        display: none;
    }
    /* Ensures long words break and wrap within the input field and chat bubbles */
    div[role="textbox"] {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    </style>
""", unsafe_allow_html=True)
