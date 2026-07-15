import streamlit as st
import requests
st.title("The AI Image Generator.")
#sidebar
st.sidebar.title("Image Generation Settings")
style=st.sidebar.selectbox("Select the style of the image you want to generate (click to see dropdown)",["Realistic","Cartoon","Anime","Fantasy","Sci-Fi","Abstract","Artistic"])
intensity=st.sidebar.slider("Select the intensity of the image (1-10)", min_value=1, max_value=10, value=5, step=1)
height=st.sidebar.slider("Select the height of the image (1-10)(1=100px and 10=1000px)", min_value=1, max_value=10, value=5, step=1)
width=st.sidebar.slider("Select the width of the image (1-10)(1=100px and 10=1000px)", min_value=1, max_value=10, value=5, step=1)

#sessin state:
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None
#input
prompt=st.text_input("Enter your prompt here:")
generate_button = st.button("Generate Image")
#generation:
if prompt and generate_button==True:
    n_prompt = f"Generate an image in the style of {style} with intensity {intensity} and height {(height)*100} and width {width*100} based on this prompt: {prompt}"
    e_prompt = requests.utils.quote(n_prompt) #query
    with st.spinner('Generating image...'):
        url=f"https://image.pollinations.ai/prompt/{e_prompt}"
        response=requests.get(url)
    if response.status_code==200:
        st.session_state.image_bytes = response.content
        st.session_state.last_prompt = prompt
        print("Successfully generated image for prompt:", prompt)
    else:
        st.warning("Failed to generate image for the given prompt. Please try again.")
elif not prompt and generate_button==True:
    st.warning("Please enter a prompt to generate an image.")

if st.session_state.image_bytes is not None:
    st.image(st.session_state.image_bytes, caption="Generated Image", use_container_width=True)
    st.download_button(
        label="Download Image",
        data=st.session_state.image_bytes,
        file_name="generated_image.png",
        mime="image/png"
    )