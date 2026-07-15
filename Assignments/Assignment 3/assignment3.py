import streamlit as st
st.title("The Multiverse Of Chatbots.")
def clear_chat_history():
    st.session_state.messages = []

#sidebar
personality=st.sidebar.selectbox("Who do you want to talk to? (click to see dropdown)",["Tenz (Valorant Esports player)","Boaster(Valorant Esports player)","Nats(Valorant Esports player)","The Goat(Literally 'Legendary')","Jaun Elia(Famouse Urdu poet)","Muhammad Ali(Famous Boxer)","Ramdhari Singh Dinkar(Famous hindi poet)"]
                                 #,on_change=clear_chat_history
                                 )
intensity=st.sidebar.slider("Select the intensity of the response (1-10)", min_value=1, max_value=10, value=5, step=1)

from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
if "messages" not in st.session_state: #Task 1: Initialize the Memory Vault
    st.session_state.messages = []
    
for message in st.session_state.messages: #Task 2: Render the Chat History
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_message := st.chat_input("Say something..."): #Task 3: Upgrade the Input UI
    with st.chat_message("user"):
        st.write(user_message)
        st.session_state.messages.append({"role": "user", "content": user_message})
        with st.spinner("Generating response..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f'''Respond to this message in the style of {personality} with intensity {intensity} 
                and totally remain in character: {user_message} 
                NOTE:EVEN IF YOU ANSWER IN ANY OTHER LANGUAGE MAKE SURE TO ROMANZISE IT BEFORE RETURNING IT.'''
            )
        with st.chat_message(personality):
            st.write(response.text)
            #Task 4: Save New Messages to Memory
            st.session_state.messages.append({"role": "assistant", "content": response.text})

