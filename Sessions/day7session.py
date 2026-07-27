import speech_recognition as sr
import streamlit as st
from streamlit_mic_recorder import speech_to_text as s_t

st. title("Internship STT")

user_voice=s_t(
    language='en',
    use_container_width="True",
    just_once=True,
    key='STT'

)

#to check if the user said something

if user_voice:
    st.write(user_voice)