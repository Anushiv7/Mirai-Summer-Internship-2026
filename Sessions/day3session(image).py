'''import streamlit as st

st.title("The Multiverse Of Chatbots.")

#sidebar
personality=st.sidebar.selectbox("Who do you want to talk to? (click to see dropdown)",["Tenz (Valorant Esports player)","Boaster(Valorant Esports player)","Nats(Valorant Esports player)","The Goat(Literally 'Legendary')","Jaun Elia(Famouse Urdu poet)","Muhammad Ali(Famous Boxer)","Ramdhari Singh Dinkar(Famous hindi poet)"])
intensity=st.sidebar.slider("Select the intensity of the response (1-10)", min_value=1, max_value=10, value=5, step=1)

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
            contents=f"Respond to this message in the style of {personality} with intensity {intensity} and totally remain in character and give a good length response: {input}"
        )
            st.write(response.text) 
    else:
        st.warning("Please enter a message before sending.")
'''

#accept prompt and generate image
'''TRYING ON MY OWN-BUT FAILED
import streamlit as st
import io
from PIL import Image

st.title("From your words to your imagination: Generate images with AI.")

#sidebar
style=st.sidebar.selectbox("Select the style of the image you want to generate (click to see dropdown)",["Realistic","Cartoon","Anime","Fantasy","Sci-Fi","Abstract"])

from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
input=st.text_input("Enter your prompt here:")

if st.button("Generate Image"):
    if input:
        st.success("Prompt recieved successfully!")
        with st.spinner("Generating image..."):
            response=client.models.generate_images(
            model="gemini-2.5-flash-image",
            prompt=f"Generate an image in the style of {style} based on this prompt: {input}"
        )#we use generate_content and contents= for text based
            generated_image = response.generated_images[0]
            image_bytes = generated_image.image.image_bytes
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption=f"Generated: {input}", use_container_width=True)
    else:
        st.warning("Please enter a prompt before generating an image.")
'''
#image.py

import requests

prompt="Boaster and Fnatic Wining Valorant Champions Tour 2025"

url=f"https://image.pollinations.ai/prompt/{prompt}"

print("Generating image for prompt:", prompt)

response=requests.get(url)

print(response)


if response.status_code==200:
    print("Sucessfully generated image for prompt:", prompt)
    with open("generated_image.png","wb") as f:
        f.write(response.content)
    print("Image saved as generated_image.png")
else:
    print("Failed to generate image for prompt:", prompt)
        