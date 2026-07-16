import streamlit as st
import requests
import random
st.title("The AI Image Generator.")
st.write('''Open the sidebar to select the settings for your image.''')

#sidebar
st.sidebar.title("Image Generation Settings")
style=st.sidebar.selectbox("Select the style of the image you want to generate (click to see dropdown)",["Realistic","Cartoon","Anime","Fantasy","Sci-Fi","Abstract","Artistic"])
intensity=st.sidebar.slider("Select the intensity of the image (1-10)", min_value=1, max_value=10, value=5, step=1)
height=st.sidebar.slider("Select the height of the image (1-10)(1=100px and 10=1000px)", min_value=1, max_value=10, value=5, step=1)
width=st.sidebar.slider("Select the width of the image (1-10)(1=100px and 10=1000px)", min_value=1, max_value=10, value=5, step=1)
me=st.sidebar.checkbox("Enable Magic Enhance ✨")
sm=st.sidebar.button("Surprise Me 🎲") #button for surprise

#surprise me intial
l1=["An astronaut riding a horse on Mars","A cyberpunk street food vendor in Tokyo","A Sushi Chef making Sushi out of exotic fish",
    "Moon dropping on the Earth like a comet",
    "A alien crying after tasting ice cream"]
     

#initialize session state:
if "history" not in st.session_state:
    st.session_state.history = []
#input
prompt=st.chat_input("Enter your prompt here:")

#working surprise me
if sm:
     prompt=(random.choice(l1)) 
     #adding magic enhance
     if me:
         prompt+=",masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"
     
     n_prompt = f"Generate an image in the style of {style} with intensity {intensity} based on this prompt: {prompt}"
     e_prompt = requests.utils.quote(n_prompt) #query
    
     with st.spinner('Generating image...'):
            url=f"https://image.pollinations.ai/prompt/{e_prompt}?width={width*100}&height={height*100}"
            response=requests.get(url)
     if response.status_code==200:
        st.session_state.history.append({
        "prompt": prompt,
        "image_bytes": response.content,
        "style": style
    })
        print("Successfully generated image for prompt:", prompt)
     else:
        st.warning("Failed to generate image for the given prompt. Please try again.")
     
#generation:
elif prompt:
        #adding magic enhance
        if me:
         prompt+=",masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"
        n_prompt = f"Generate an image in the style of {style} with intensity {intensity} based on this prompt: {prompt}"
        e_prompt = requests.utils.quote(n_prompt) #query
        with st.spinner('Generating image...'):
            url=f"https://image.pollinations.ai/prompt/{e_prompt}?width={width*100}&height={height*100}"
            response=requests.get(url)
        if response.status_code==200:
            st.session_state.history.append({
            "prompt": prompt,
            "image_bytes": response.content,
            "style": style
        })
            print("Successfully generated image for prompt:", prompt)
        else:
            st.warning("Failed to generate image for the given prompt. Please try again.")
elif not prompt and not st.session_state.history:
    st.text("Please enter a prompt to generate an image.")

#session state display
for index, item in enumerate(st.session_state.history):
    st.write(f"**Prompt:** {item['prompt']}")
    st.image(
        item['image_bytes'], 
        caption=f"Generated Image {index + 1}", 
        use_container_width=True
    )
    image_style = item.get('style')
    st.download_button(
        label=f"Download Image {index + 1}",
        data=item['image_bytes'],
        file_name=f"my_ai_image_{image_style}_{index + 1}.png",
        mime="image/png",
        key=f"download_btn_{index}"
    )