import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from datetime import date


load_dotenv()
st.title("The AI Chat with Memory Vault.")

@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client= get_ai_client()

#initialize session state:
if "messages" not in st.session_state:
    st.session_state.messages = []

if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat=client.chats.create(model="gemini-2.5-flash")

#display chat messages from history on app rerun
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])  

#accept new user input
if user_input := st.chat_input("Enter your message here:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("Thinking..."):
        response=st.session_state.gemini_chat.send_message(user_input)
        assistant_response=response.text
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.chat_message("AI").write(assistant_response)


st.download_button(
        label="Download Chat",
        data="\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages]),
        file_name=f"chat_history.txt:{date.today()}",
        mime="text/plain",
        key="download_chat_button"
        )

#'''Alternative:
#output="CHAT HISTORY"
#
#for mssg in st.session_state.messages: 
#   output+=f"\n{msg['role]....}'''
#st.download_button(
#    label="Download Chat",
#   data=output,
#    file_name=f"chat_history.txt:{date.today()}",
#   mime="text/plain"
#)

