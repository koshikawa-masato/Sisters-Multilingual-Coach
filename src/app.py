"""
Sisters-Multilingual-Coach - Main Streamlit App
Learn languages through conversation with the Three Sisters
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Sisters Multilingual Coach",
    page_icon="🌏",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_sister" not in st.session_state:
    st.session_state.current_sister = "Botan"
if "target_language" not in st.session_state:
    st.session_state.target_language = "English"

# Sisters profiles
SISTERS = {
    "Botan": {
        "emoji": "🌸",
        "personality": "Sociable, trendy, LA returnee",
        "best_for": "Casual conversation, trends, entertainment",
        "color": "#FF69B4"
    },
    "Kasho": {
        "emoji": "🎵",
        "personality": "Professional, logical, music expert",
        "best_for": "Business language, formal speech",
        "color": "#4169E1"
    },
    "Yuri": {
        "emoji": "📚",
        "personality": "Creative, bookworm, subculture expert",
        "best_for": "Literature, culture, creative expression",
        "color": "#9370DB"
    }
}

LANGUAGES = ["English", "中文", "日本語", "한국어", "Español"]

# Sidebar
with st.sidebar:
    st.title("🌏 Settings")

    # Language selection
    st.subheader("Target Language")
    target_lang = st.selectbox(
        "I want to practice:",
        LANGUAGES,
        index=LANGUAGES.index(st.session_state.target_language)
    )
    st.session_state.target_language = target_lang

    st.divider()

    # Sister selection
    st.subheader("Chat Partner")
    for name, info in SISTERS.items():
        if st.button(
            f"{info['emoji']} {name}",
            use_container_width=True,
            type="primary" if st.session_state.current_sister == name else "secondary"
        ):
            st.session_state.current_sister = name
            st.rerun()

    # Show current sister info
    current = SISTERS[st.session_state.current_sister]
    st.divider()
    st.markdown(f"**{current['emoji']} {st.session_state.current_sister}**")
    st.caption(current["personality"])
    st.caption(f"Best for: {current['best_for']}")

    st.divider()

    # Voice settings
    st.subheader("Voice Settings")
    voice_enabled = st.toggle("Enable TTS", value=True)
    auto_listen = st.toggle("Auto-listen after response", value=False)

# Main content
st.title(f"🌏 Sisters Multilingual Coach")
st.caption(f"Practice {st.session_state.target_language} with {st.session_state.current_sister}")

# Chat container
chat_container = st.container()

with chat_container:
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=msg.get("avatar")):
            st.markdown(msg["content"])

# Input area
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.chat_input(f"Type in {st.session_state.target_language}...")

with col2:
    mic_button = st.button("🎤 Speak", use_container_width=True)

# Handle text input
if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # TODO: Send to LLM and get response
    # For now, placeholder response
    sister = st.session_state.current_sister
    sister_info = SISTERS[sister]

    # Placeholder response (will be replaced with actual LLM call)
    if st.session_state.target_language == "English":
        response = f"Hi! I'm {sister}. I heard you say: '{user_input}'. Let's practice English together!"
    elif st.session_state.target_language == "中文":
        response = f"你好！我是{sister}。你說：'{user_input}'。讓我們一起練習中文吧！"
    else:
        response = f"Hello! I'm {sister}. You said: '{user_input}'"

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "avatar": sister_info["emoji"]
    })

    st.rerun()

# Handle microphone input
if mic_button:
    st.info("🎤 Voice input coming soon! (Whisper STT integration)")

# Footer
st.divider()
st.caption("Sisters-Multilingual-Coach v0.1.0 | Powered by ElevenLabs TTS + Whisper STT")
