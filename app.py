import random
import urllib.parse
import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🎨 AI Image Studio")
st.caption("Turn your imagination into images with AI.")


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Image Settings")


# Art Style
art_style = st.sidebar.selectbox(
    "🎨 Art Style",
    [
        "Realistic",
        "Anime",
        "Digital Art",
        "Oil Painting",
        "Cyberpunk",
        "3D Render",
        "Watercolor",
        "Fantasy"
    ]
)


# ============================================================
# TASK 1 — WIDTH & HEIGHT SLIDERS
# ============================================================

width = st.sidebar.slider(
    "↔️ Image Width",
    min_value=256,
    max_value=1536,
    value=1024,
    step=128
)

height = st.sidebar.slider(
    "↕️ Image Height",
    min_value=256,
    max_value=1536,
    value=1024,
    step=128
)


# ============================================================
# TASK 3 — MAGIC ENHANCE
# ============================================================

magic_enhance = st.sidebar.checkbox(
    "✨ Enable Magic Enhance"
)


# ============================================================
# TASK 4 — SURPRISE ME PROMPTS
# ============================================================

surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A magical forest floating above the clouds",
    "A futuristic underwater city with glowing buildings",
    "A dragon protecting an ancient library at midnight"
]


# ============================================================
# PROMPT
# ============================================================

st.subheader("✍️ Describe Your Image")

user_prompt = st.text_area(
    "Enter your image prompt",
    placeholder="Example: A futuristic Indian palace floating above the clouds...",
    height=120
)


# ============================================================
# IMAGE GENERATION
# ============================================================

def generate_image(
    prompt,
    style,
    image_width,
    image_height,
    enhance=False
):

    # Add selected art style
    full_prompt = f"{prompt}, {style} art style"

    # --------------------------------------------------------
    # TASK 3 — MAGIC ENHANCE
    # --------------------------------------------------------

    if enhance:
        full_prompt += (
            ", masterpiece, 8k resolution, highly detailed, "
            "trending on artstation, unreal engine 5 render"
        )

    # Encode prompt
    encoded_prompt = urllib.parse.quote(full_prompt)

    # --------------------------------------------------------
    # TASK 1 — WIDTH + HEIGHT
    #
    # This is the exact fix requested by the assignment.
    # --------------------------------------------------------

    image_url = (
        f"https://image.pollinations.ai/prompt/"
        f"{encoded_prompt}"
        f"?width={image_width}&height={image_height}"
    )

    try:

        response = requests.get(
            image_url,
            timeout=120
        )

        if response.status_code == 200:

            return image_url, response.content

        st.error(
            f"Image generation failed. "
            f"Server returned status code {response.status_code}."
        )

        return None, None

    except Exception as e:

        st.error(
            f"Error generating image: {e}"
        )

        return None, None


# ============================================================
# BUTTONS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    generate_button = st.button(
        "🎨 Generate Image",
        use_container_width=True
    )


with col2:

    surprise_button = st.button(
        "🎲 Surprise Me!",
        use_container_width=True
    )


# ============================================================
# TASK 4 — SURPRISE ME
# ============================================================

if surprise_button:

    random_prompt = random.choice(
        surprise_prompts
    )

    st.info(
        f"🎲 Surprise Prompt: **{random_prompt}**"
    )

    image_url, image_data = generate_image(
        random_prompt,
        art_style,
        width,
        height,
        magic_enhance
    )

    if image_data:

        st.session_state.generated_image = image_data
        st.session_state.generated_url = image_url
        st.session_state.generated_prompt = random_prompt
        st.session_state.generated_style = art_style
        st.session_state.generated_width = width
        st.session_state.generated_height = height


# ============================================================
# NORMAL GENERATION
# ============================================================

elif generate_button:

    if not user_prompt.strip():

        st.warning(
            "⚠️ Please enter a prompt first."
        )

    else:

        image_url, image_data = generate_image(
            user_prompt,
            art_style,
            width,
            height,
            magic_enhance
        )

        if image_data:

            st.session_state.generated_image = image_data
            st.session_state.generated_url = image_url
            st.session_state.generated_prompt = user_prompt
            st.session_state.generated_style = art_style
            st.session_state.generated_width = width
            st.session_state.generated_height = height


# ============================================================
# DISPLAY IMAGE
# ============================================================

if "generated_image" in st.session_state:

    st.divider()

    st.subheader("🖼️ Generated Image")

    st.image(
        st.session_state.generated_image,
        caption=(
            f"{st.session_state.generated_style} | "
            f"{st.session_state.generated_width} × "
            f"{st.session_state.generated_height}"
        ),
        use_container_width=True
    )


    # ========================================================
    # TASK 2 — PNG DOWNLOAD
    # ========================================================

    safe_style = (
        st.session_state.generated_style
        .lower()
        .replace(" ", "_")
    )

    file_name = f"{safe_style}_ai_image.png"


    st.download_button(
        label="⬇️ Download Image",
        data=st.session_state.generated_image,
        file_name=file_name,
        mime="image/png",
        use_container_width=True
    )

    st.success(
        f"✅ Image ready to download as `{file_name}`"
    )