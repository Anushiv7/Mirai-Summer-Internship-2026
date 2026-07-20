import json
import os
import urllib.parse
from datetime import date
from io import BytesIO

from dotenv import load_dotenv
from google import genai
from gtts import gTTS
import requests
import streamlit as st
import re


# Load environment variables
load_dotenv()

st.set_page_config(page_title="AI Visual Novel Engine", page_icon="📖", layout="centered")
st.title("📖 The AI Visual Novel Engine")

# ==========================================
# PHASE 1: UI, Caching & Settings
# ==========================================

# 1. Cache the Gemini Client
@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_ai_client()

# 2. Sidebar Configuration
st.sidebar.title("Story Settings")
a_style = st.sidebar.selectbox(
    "Select Art Style",
    [
        "Anime",
        "Realistic",
        "Cartoon",
        "Fantasy",
        "Sci-Fi",
        "Pixel Art",
        "Digital Oil Painting",
    ],
)
s_genre = st.sidebar.selectbox(
    "Select Story Genre",
    [
        "Fantasy",
        "Sci-Fi",
        "Political",
        "Self Help",
        "Inspirational",
        "Child Friendly",
    ],
)

# 3. System Instructions forcing JSON structure
system_instructions = f"""
You are an interactive Visual Novel AI storyteller.
Genre: {s_genre}
Art Style: {a_style}

You must ALWAYS respond ONLY with a single valid JSON object containing these keys:
1. "story_text": A narrative paragraph continuing the story.
2. "image_prompt": A visual description in {a_style} style suitable for image generation.
3. "options": A Python list of 2 to 3 distinct action choices for the user.

Output raw JSON only. Do NOT use markdown code blocks like ```json.
"""

# 4. Initialize Session State
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": system_instructions},
    )

if "current_scene" not in st.session_state:
    st.session_state.current_scene = None

if "scenes_list" not in st.session_state:
    st.session_state.scenes_list = []

if "story_history" not in st.session_state:
    st.session_state.story_history = []


# ==========================================
# PHASE 2: Structured JSON Engine Helper
# ==========================================
def get_next_scene(user_text):
    raw_response = st.session_state.gemini_chat.send_message(user_text).text
    
    # 1. Clean code fences
    clean_text = (
        raw_response.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )

    # 2. Extract ONLY the JSON object between the first '{' and the last '}'
    match = re.search(r'\{.*\}', clean_text, re.DOTALL)
    if match:
        clean_text = match.group(0)

    # 3. Parse safely
    try:
        parsed_scene = json.loads(clean_text)
    except json.JSONDecodeError:
        # Fallback in case JSON is somehow mangled
        parsed_scene = {
            "story_text": clean_text,
            "image_prompt": "fantasy landscape",
            "options": ["Continue"]
        }

    # Save to history
    st.session_state.scenes_list.append(parsed_scene)
    st.session_state.story_history.append(
        f"User Choice: {user_text}\nStory: {parsed_scene.get('story_text', '')}\n"
    )

    return parsed_scene 


# ==========================================
# LANDING SCREEN vs. GAMEPLAY LOOP
# ==========================================

# Show Start Screen if game hasn't started yet
if st.session_state.current_scene is None:
    st.info("👈 Customize your **Genre** and **Art Style** in the sidebar, then hit start to begin!")
    
    if st.button("🚀 Start Adventure", type="primary"):
        with st.spinner("Generating your opening scene..."):
            st.session_state.current_scene = get_next_scene("Begin the story.")
            st.rerun()

# Once game starts, render story and choices
else:
    # ----------------------------------------------------
    # SCROLLABLE CONTAINER (Holds all previous chapters)
    # ----------------------------------------------------
    with st.container(height=520):
        for chapter_num, scene in enumerate(st.session_state.scenes_list, start=1):
            st.subheader(f"Chapter {chapter_num}")
            st.write(scene["story_text"])

            # --- Phase 4 & 5: Text-To-Speech (Audio) ---
            try:
                tts = gTTS(text=scene["story_text"], lang="en")
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes, format="audio/mp3")
            except Exception:
                st.toast("Could not generate audio narration.")

            # --- Phase 4 & 5: Pollinations Visuals (Fixed Headers & Timeout) ---
            try:
                clean_prompt = scene["image_prompt"].replace("\n", " ")
                prompt_encoded = urllib.parse.quote(f"{clean_prompt}, {a_style} style")
                image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=1024&height=1024&nologo=true"

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
                }

                img_res = requests.get(image_url, headers=headers, timeout=12)

                if img_res.status_code == 200:
                    st.image(img_res.content, caption=f"Scene {chapter_num} Visual")
                else:
                    st.toast("Image server is busy, skipping visual...")
            except Exception:
                st.toast("Image server timeout or busy, skipping visual...")

            st.divider()

    # ----------------------------------------------------
    # FIXED BOTTOM SECTION (Always visible choices)
    # ----------------------------------------------------
    latest_scene = st.session_state.scenes_list[-1]

    st.subheader("What do you do next?")

    # Dynamic action buttons based on latest scene options
    for idx, choice in enumerate(latest_scene.get("options", [])):
        # Key uses total scenes length so buttons don't collide between turns
        button_key = f"btn_{len(st.session_state.scenes_list)}_{idx}"
        
        if st.button(choice, key=button_key, use_container_width=True):
            with st.spinner("The story progresses..."):
                st.session_state.current_scene = get_next_scene(choice)
                st.rerun()

    # Restart option in sidebar
    if st.sidebar.button("🔄 Restart Story"):
        st.session_state.current_scene = None
        st.session_state.scenes_list = []
        st.session_state.story_history = []
        st.rerun()

# --- Sidebar Download Feature ---
if st.session_state.story_history:
    st.sidebar.divider()
    st.sidebar.download_button(
        label="Download Story Log",
        data="\n-------------------\n".join(st.session_state.story_history),
        file_name=f"story_log_{date.today()}.txt",
        mime="text/plain",
    )