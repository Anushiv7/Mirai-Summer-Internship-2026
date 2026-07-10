""""import streamlit as st
import os
from dotenv import load_dotenv 
load_dotenv()
env_var=os.getenv("GEMINI_API_KEY")
print("env_var",#use env_var in your code to show the api key..in this case i'm redacting it bcs it can't be made public.)
"""
import streamlit as st

st.title("The Multiverse Of Chatbots.")
personality=st.selectbox("Who do you want to talk to? (click to see dropdown)",["Tenz (Valorant Esports player)","Boaster(Valorant Esports player)","Nats(Valorant Esports player)","The Goat(Literally 'Legendary')","Jaun Elia(Famouse Urdu poet)","Muhammad Ali(Famous Boxer)","Ramdhari Singh Dinkar(Famous hindi poet)"])

from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
input=st.text_input("Enter your message here:")
if st.button("Send"):
    if input:
        st.success("Message recieved successfully!")
        with st.spinner("Generating response..."):
            response=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Respond to this message in the style of {personality} and totally remain in character and give a good length response: {input}"
        )
            st.write(response.text)
    else:
        st.warning("Please enter a message before sending.")

        

