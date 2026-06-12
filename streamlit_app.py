import streamlit as st
import base64
import time

from agent import process_message

# =====================================
# Page Config
# =====================================

st.set_page_config(
    page_title="AI Customer Support Agent",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# Background Image Loader
# =====================================

def get_base64(image_path):

    with open(image_path, "rb") as img:

        return base64.b64encode(
            img.read()
        ).decode()

bg_image = get_base64(
    "assets/background.png")


# =====================================
# Custom CSS
# =====================================

st.markdown(
f"""
<style>

/* =====================================
BACKGROUND IMAGE
===================================== */

.stApp {{

    background-image:
    url("data:image/png;base64,{bg_image}");

    background-size: cover;

    background-position: center;

    background-repeat: no-repeat;

    background-attachment: fixed;

}}

/* =====================================
SPARKLING STARS
===================================== */

.stApp::before {{

    content: "";

    position: fixed;

    top: 0;
    left: 0;

    width: 100%;
    height: 100%;

    background-image:

        radial-gradient(circle, white 1px, transparent 2px),
        radial-gradient(circle, white 2px, transparent 3px),
        radial-gradient(circle, white 1px, transparent 2px),
        radial-gradient(circle, white 2px, transparent 3px);

    background-size:
        150px 150px,
        250px 250px,
        350px 350px,
        500px 500px;

    background-position:
        20px 40px,
        100px 200px,
        300px 100px,
        600px 300px;

    animation:
        twinkle 4s ease-in-out infinite;

    opacity: 0.8;

    z-index: -1;
}}

@keyframes twinkle {{

    0% {{

        opacity: 0.2;

    }}

    25% {{

        opacity: 0.8;

    }}

    50% {{

        opacity: 0.4;

    }}

    75% {{

        opacity: 1;

    }}

    100% {{

        opacity: 0.2;

    }}

}}
/* =====================================
SIDEBAR
===================================== */

[data-testid="stSidebar"] {{

    background:
    rgba(0,0,0,0.25);

    backdrop-filter:
    blur(25px);

    border-right:
    1px solid rgba(255,255,255,0.1);

}}

/* =====================================
CHAT MESSAGES
===================================== */

[data-testid="stChatMessage"] {{

    background:
    rgba(255,255,255,0.08);

    backdrop-filter:
    blur(20px);

    border-radius: 20px;

    padding: 12px;

    margin-bottom: 10px;

    animation:
    fadeUp 0.4s ease;

}}

@keyframes fadeUp {{

    from {{

        opacity: 0;

        transform:
        translateY(20px);

    }}

    to {{

        opacity: 1;

        transform:
        translateY(0);

    }}

}}

/* =====================================
CHAT INPUT
===================================== */

[data-testid="stChatInput"] {{

    background:
    rgba(255,255,255,0.08);

    backdrop-filter:
    blur(20px);

    border-radius: 20px;

}}

/* =====================================
TITLE
===================================== */

h1 {{

    color: white;

    text-align: center;

    text-shadow:
    0 0 20px #60a5fa,
    0 0 40px #38bdf8,
    0 0 80px #38bdf8;

}}

/* =====================================
TEXT
===================================== */

p, div, span {{

    color: white;

}}

</style>
""",
unsafe_allow_html=True
)

# =====================================
# Title
# =====================================

st.markdown(
    "<h1>🌌 AI Customer Support Agent</h1>",
    unsafe_allow_html=True
)

# =====================================
# Sidebar
# =====================================

with st.sidebar:

    st.header("⚙️ Support Tools")

    st.write(
        "Track Orders"
    )

    st.write(
        "Cancel Orders"
    )

    st.write(
        "Return Products"
    )

    st.write(
        "Refund Status"
    )

# =====================================
# Chat History
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =====================================
# Display Messages
# =====================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# =====================================
# Chat Input
# =====================================

prompt = st.chat_input(
    "Ask me anything..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    response = process_message(
        prompt
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    with st.chat_message("assistant"):

        st.markdown(response)