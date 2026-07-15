import streamlit as st
import requests
st.title("The AI Image Generator.")
st.write('''Open the sidebar to select the settings for your image.''')
#sidebar
st.sidebar.title("Image Generation Settings")
style=st.sidebar.selectbox("Select the style of the image you want to generate (click to see dropdown)",["Realistic","Cartoon","Anime","Fantasy","Sci-Fi","Abstract","Artistic"])
intensity=st.sidebar.slider("Select the intensity of the image (1-10)", min_value=1, max_value=10, value=5, step=1)
height=st.sidebar.slider("Select the height of the image (1-10)(1=100px and 10=1000px)", min_value=1, max_value=10, value=5, step=1)
width=st.sidebar.slider("Select the width of the image (1-10)(1=100px and 10=1000px)", min_value=1, max_value=10, value=5, step=1)

#initialize session state:
if "history" not in st.session_state:
    st.session_state.history = []
#input
prompt=st.chat_input("Enter your prompt here:")

#generation:
if prompt:
        n_prompt = f"Generate an image in the style of {style} with intensity {intensity} and height {(height)*100} and width {width*100} based on this prompt: {prompt}"
        e_prompt = requests.utils.quote(n_prompt) #query
        with st.spinner('Generating image...'):
            url=f"https://image.pollinations.ai/prompt/{e_prompt}"
            response=requests.get(url)
        if response.status_code==200:
            st.session_state.history.append({
            "prompt": prompt,
            "image_bytes": response.content
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
    st.download_button(
        label=f"Download Image {index + 1}",
        data=item['image_bytes'],
        file_name=f"generated_image_{index + 1}.png",
        mime="image/png",
        key=f"download_btn_{index}"
    )