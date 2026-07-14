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

''''Assignment Instructions:
MirAI School of Technology
Virtual Summer Internship 2026: The "AI Builder" Track
Assignment : The Memory Vault (Stateful Chatbot)
Submit a screen recording demonstrating a continuous 3-message conversation and your updated app.py code to the student portal.

Objective
Up to this point, your Multiverse Chatbot has suffered from severe amnesia. Because of Streamlit's architecture, every time you click "SEND" or change a slider, the entire Python script reruns from top to bottom, wiping out your previous conversation.

Your objective for this assignment is to upgrade your application from a stateless app (forgets everything) to a stateful app (remembers history). You will achieve this using Streamlit's

"Memory Vault": st.session_state.

Core Requirements
Modify your existing app.py chatbot file to complete the following tasks:
Task 1: Initialize the Memory Vault
Before you can display or save messages, you need to create a place to store them that survives page reloads.

● At the top of your script (below your API initialization), write an if statement to check if "messages" exists in st.session_state.

● If it does not exist, initialize st.session_state.messages as an empty Python list [].

Task 2: Render the Chat History
Your app needs to redraw all past messages every time the script reruns.

● Create a for loop that iterates through every message stored in
st.session_state.messages.

● Inside the loop, use st.chat_message() to display both the role (user/assistant) and the text of the message on the screen.

Task 3: Upgrade the Input UI
The old st.text_input() and st.button("SEND") combo is outdated for chat interfaces.
● Delete your st.text_input and st.button logic.
● Replace them with Streamlit's native chat input component: st.chat_input("Say something...").
● Hint: You will need to use the walrus operator (:=) to assign the input to a variable and check if it has data in a single line. Example: if user_message := st.chat_input("Say something:"):

Task 4: Save New Messages to Memory
When the user types a new message and the AI generates a response, you must save both to the vault so they aren't lost on the next rerun.

● Immediately after the user sends a message, append it to st.session_state.messages as a dictionary: {"role": "user", "content": user_message}.

● After the Gemini API returns its response, append the AI's response to the same list:
{"role": "assistant", "content": response.text}.

📚 Essential Resource Links
As an engineer, reading official documentation is a mandatory skill. You will need to review these pages to complete this assignment:

1. Session State Basics: https://docs.streamlit.io/library/api-reference/session-state
○ Read this to understand how to store variables so they don't disappear.

2. Chat Elements Documentation: https://docs.streamlit.io/library/api-reference/chat
○ Read this to see exactly how st.chat_input and st.chat_message interact.
3. Tutorial: Build a Basic LLM App:
https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
○ This is your ultimate cheat sheet. It contains the exact structural logic you need to build a stateful chat UI.
Pre-Submission Checklist
● Does your app successfully remember the very first message even after you send a third or fourth message?
● Did you successfully replace the "SEND" button with st.chat_input?
● Does changing the sidebar personality dropdown keep the chat history on the screen, or does it wipe it out? (It should keep it!)
Cancel'''