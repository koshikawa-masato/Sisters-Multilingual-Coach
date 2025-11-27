"""
Sisters-Multilingual-Coach - Complete Learning Flow
Goal: 英会話ができるようになる！
"""

import streamlit as st
import os
import json
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Sisters Multilingual Coach",
    page_icon="🌏",
    layout="wide"
)

# Initialize providers (lazy loading)
@st.cache_resource
def get_kimi():
    from llm import KimiLLM
    return KimiLLM()

def get_tts():
    # No cache - ensure fresh instance with updated code
    from tts import ElevenLabsTTS
    return ElevenLabsTTS()

@st.cache_resource
def get_stt():
    from stt import WhisperSTT
    return WhisperSTT()

# Session state initialization
def init_session_state():
    defaults = {
        "step": 1,
        "japanese_text": "",
        "english_text": "",
        "corrected_text": "",
        "writing_feedback": None,
        "spoken_text": "",
        "speaking_feedback": None,
        "sister_responses": None,  # Changed: Store all 3 sisters' responses
        "quiz": None,
        "quiz_answer": None,
        "current_sister": "Botan",
        "target_language": "English",
        "conversation_history": [],
        "audio_data": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Characters profiles
SISTERS = {
    "Botan": {"emoji": "🌸", "desc": "Casual conversation, trends"},
    "Kasho": {"emoji": "🎵", "desc": "Business, formal speech"},
    "Yuri": {"emoji": "💻", "desc": "Technology, programming"},
    "Ojisan": {"emoji": "👨", "desc": "Typical American uncle, friendly"}
}

# Sidebar
with st.sidebar:
    st.title("🌏 Settings")

    st.subheader("Sister")
    for name, info in SISTERS.items():
        if st.button(
            f"{info['emoji']} {name}",
            use_container_width=True,
            type="primary" if st.session_state.current_sister == name else "secondary"
        ):
            st.session_state.current_sister = name
            st.session_state.audio_data = None  # Clear cached audio when switching sister
            st.rerun()

    st.caption(f"Best for: {SISTERS[st.session_state.current_sister]['desc']}")

    st.divider()

    st.subheader("Progress")
    steps = ["①日本語", "②Writing", "③添削", "④Speaking", "⑤発音添削", "⑥Listening", "⑦Reading", "⑧Quiz", "⑨Feedback"]
    current = st.session_state.step
    for i, step in enumerate(steps, 1):
        if i < current:
            st.markdown(f"~~{step}~~ ✅")
        elif i == current:
            st.markdown(f"**→ {step}**")
        else:
            st.markdown(f"{step}")

    st.divider()
    if st.button("🔄 Start Over", use_container_width=True):
        # Preserve current_sister selection
        current_sister = st.session_state.get("current_sister", "Botan")
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.current_sister = current_sister
        st.rerun()

# Main content
st.title(f"🌏 Sisters Multilingual Coach")
st.caption(f"🎯 Goal: 英会話ができるようになる！ | Partner: {SISTERS[st.session_state.current_sister]['emoji']} {st.session_state.current_sister}")

# ===========================================
# STEP 1: Japanese Input
# ===========================================
if st.session_state.step == 1:
    st.header("① 日本語で伝えたい内容を書く")
    st.caption("💡 Ctrl+Enter で次へ進めます")

    with st.form("step1_form"):
        japanese_input = st.text_area(
            "何を言いたいですか？",
            value=st.session_state.japanese_text,
            placeholder="例: 明日、買い物に行きたいな",
            height=100
        )
        submitted = st.form_submit_button("次へ ▶", type="primary")

        if submitted and japanese_input:
            st.session_state.japanese_text = japanese_input
            st.session_state.step = 2
            st.rerun()

# ===========================================
# STEP 2: English Writing
# ===========================================
elif st.session_state.step == 2:
    st.header("② 英語で書いてみましょう【Writing】")
    st.caption("💡 Ctrl+Enter で添削へ進めます")

    st.info(f"💬 伝えたいこと: 「{st.session_state.japanese_text}」")

    # Back button outside form
    if st.button("◀ 戻る"):
        st.session_state.step = 1
        st.rerun()

    with st.form("step2_form"):
        english_input = st.text_area(
            "英語で書いてください",
            value=st.session_state.english_text,
            placeholder="例: I want to go shopping tomorrow",
            height=100
        )
        submitted = st.form_submit_button("添削する ✓ (Ctrl+Enter)", type="primary", use_container_width=True)

        if submitted and english_input:
            st.session_state.english_text = english_input
            st.session_state.step = 3
            st.rerun()

# ===========================================
# STEP 3: Writing Correction
# ===========================================
elif st.session_state.step == 3:
    st.header("③ Kimi が添削します")

    with st.spinner("添削中..."):
        if st.session_state.writing_feedback is None:
            try:
                kimi = get_kimi()
                feedback = kimi.correct_writing(
                    st.session_state.japanese_text,
                    st.session_state.english_text
                )
                st.session_state.writing_feedback = feedback
                st.session_state.corrected_text = feedback.get("corrected", st.session_state.english_text)
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.writing_feedback = {
                    "original": st.session_state.english_text,
                    "corrected": st.session_state.english_text,
                    "is_correct": True,
                    "corrections": [],
                    "rating": 3,
                    "encouragement_jp": "添削サービスに接続できませんでした"
                }
                st.session_state.corrected_text = st.session_state.english_text

    feedback = st.session_state.writing_feedback

    # Show results
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your writing:")
        st.info(feedback.get("original", st.session_state.english_text))

    with col2:
        st.subheader("Corrected:")
        if feedback.get("is_correct"):
            st.success(feedback.get("corrected", ""))
        else:
            st.warning(feedback.get("corrected", ""))

    # Show corrections
    corrections = feedback.get("corrections", [])
    if corrections:
        st.subheader("📝 Corrections:")
        for c in corrections:
            st.markdown(f"- **{c.get('error', '')}** → {c.get('fix', '')}")
            st.caption(f"  💡 {c.get('explanation_jp', '')}")

    # Rating
    rating = feedback.get("rating", 3)
    st.markdown(f"**Rating:** {'⭐' * rating}")
    st.info(f"💪 {feedback.get('encouragement_jp', '頑張りましょう！')}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("◀ 書き直す"):
            st.session_state.writing_feedback = None
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("発音練習へ ▶", type="primary"):
            st.session_state.step = 4
            st.rerun()

# ===========================================
# STEP 4: Speaking Practice
# ===========================================
elif st.session_state.step == 4:
    st.header("④ 読み上げましょう【Speaking】")
    st.caption("💡 Ctrl+Enter で発音チェックへ進めます")

    st.success(f"📖 Read this aloud: **{st.session_state.corrected_text}**")

    # Listen to example first (using User/Sam voice for example)
    st.subheader("🔊 お手本を聴く (Sam)")
    if st.button("▶ Play Example"):
        try:
            tts = get_tts()
            audio_bytes = tts.generate_speech(
                st.session_state.corrected_text,
                sister="User"  # Use Sam (male) voice for example
            )
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.error(f"TTS Error: {e}")

    st.divider()

    # Record user speech
    st.subheader("🎤 あなたの番です")

    # Back button outside form
    if st.button("◀ 戻る"):
        st.session_state.step = 3
        st.rerun()

    # Text input with form for Ctrl+Enter
    with st.form("step4_form"):
        st.caption("読み上げた英語を入力してください:")
        spoken_demo = st.text_input(
            "What you said:",
            value=st.session_state.corrected_text,  # Pre-fill with target
            placeholder="I want to go shopping tomorrow"
        )
        submitted = st.form_submit_button("発音チェック ✓ (Ctrl+Enter)", type="primary", use_container_width=True)

        if submitted and spoken_demo:
            st.session_state.spoken_text = spoken_demo
            st.session_state.step = 5
            st.rerun()

# ===========================================
# STEP 5: Speaking Correction
# ===========================================
elif st.session_state.step == 5:
    st.header("⑤ 発音チェック【Speaking Feedback】")

    with st.spinner("発音を分析中..."):
        if st.session_state.speaking_feedback is None:
            try:
                kimi = get_kimi()
                feedback = kimi.correct_speaking(
                    st.session_state.corrected_text,
                    st.session_state.spoken_text
                )
                st.session_state.speaking_feedback = feedback
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.speaking_feedback = {
                    "target": st.session_state.corrected_text,
                    "spoken": st.session_state.spoken_text,
                    "accuracy_percent": 100,
                    "word_comparison": [],
                    "overall_feedback_jp": "分析できませんでした",
                    "focus_point_jp": "もう一度試してください"
                }

    feedback = st.session_state.speaking_feedback

    # Show comparison
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Target:")
        st.code(feedback.get("target", ""))

    with col2:
        st.subheader("🎤 You said:")
        accuracy = feedback.get("accuracy_percent", 100)
        if accuracy >= 90:
            st.success(feedback.get("spoken", ""))
        elif accuracy >= 70:
            st.warning(feedback.get("spoken", ""))
        else:
            st.error(feedback.get("spoken", ""))

    # Accuracy meter
    st.metric("Accuracy", f"{accuracy}%")
    st.progress(accuracy / 100)

    # Word comparison
    word_comparison = feedback.get("word_comparison", [])
    if word_comparison:
        st.subheader("📝 Word by Word:")
        for w in word_comparison:
            icon = "✅" if w.get("correct") else "❌"
            st.markdown(f"{icon} **{w.get('target', '')}** → {w.get('spoken', '')}")
            if not w.get("correct") and w.get("tip_jp"):
                st.caption(f"  💡 {w.get('tip_jp', '')}")

    # Overall feedback
    st.info(f"📊 {feedback.get('overall_feedback_jp', '')}")
    st.warning(f"🎯 次回のポイント: {feedback.get('focus_point_jp', '')}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("◀ もう一度話す"):
            st.session_state.speaking_feedback = None
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("🔄 Try Again"):
            st.session_state.speaking_feedback = None
            st.session_state.spoken_text = ""
            st.session_state.step = 4
            st.rerun()
    with col3:
        if st.button("会話へ進む ▶", type="primary"):
            st.session_state.step = 6
            st.rerun()

# ===========================================
# STEP 6: Sister Response (Listening)
# ===========================================
elif st.session_state.step == 6:
    st.header(f"⑥ キャラクターの返答【Listening】")
    st.caption(f"💡 左のメニューでキャラクターを切り替えると、それぞれの視点で答えます")

    # Generate responses from ALL characters
    if st.session_state.sister_responses is None:
        st.session_state.sister_responses = {}

        with st.spinner("みんなが考え中..."):
            kimi = get_kimi()
            for sister_name in SISTERS.keys():
                try:
                    response = kimi.sister_response(
                        sister_name,
                        st.session_state.corrected_text,
                        st.session_state.conversation_history
                    )
                    st.session_state.sister_responses[sister_name] = response
                except Exception as e:
                    st.error(f"{sister_name} Error: {e}")
                    st.session_state.sister_responses[sister_name] = {
                        "response_en": f"That sounds interesting! Tell me more.",
                        "response_jp": "面白そう！もっと教えてください。",
                        "words_to_highlight": ["interesting", "more"]
                    }

    # Get current sister's response
    current_sister = st.session_state.current_sister
    response = st.session_state.sister_responses.get(current_sister, {})
    response_en = response.get("response_en", "")

    # Show current sister indicator
    st.success(f"{SISTERS[current_sister]['emoji']} **{current_sister}** の返答")

    # Display with word highlighting
    st.subheader("🔊 Listen:")

    # TTS Playback
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶ Play", use_container_width=True):
            try:
                current_sister = st.session_state.current_sister
                print(f"[STEP 6] Play clicked - Sister: {current_sister}")  # Debug
                tts = get_tts()
                print(f"[STEP 6] TTS instance created, calling generate_speech with sister={current_sister}")  # Debug
                audio_bytes = tts.generate_speech(
                    response_en,
                    sister=current_sister
                )
                st.session_state.audio_data = audio_bytes
                print(f"[STEP 6] Audio generated successfully, {len(audio_bytes)} bytes")  # Debug
            except Exception as e:
                st.error(f"TTS Error: {e}")
                print(f"[STEP 6] TTS Error: {e}")  # Debug

    with col2:
        if st.button("🐢 Slow", use_container_width=True):
            st.info("Slow playback coming soon!")

    with col3:
        if st.button("🔁 Repeat", use_container_width=True):
            if st.session_state.audio_data:
                st.audio(st.session_state.audio_data, format="audio/mp3")

    if st.session_state.audio_data:
        st.audio(st.session_state.audio_data, format="audio/mp3")

    # Show English with highlights
    st.divider()
    words_to_highlight = response.get("words_to_highlight", [])

    # Create highlighted text
    highlighted_html = response_en
    for word in words_to_highlight:
        highlighted_html = highlighted_html.replace(
            word,
            f'<span style="background-color: #FFEB3B; padding: 2px 4px; border-radius: 3px;">{word}</span>'
        )

    st.markdown(f"### {highlighted_html}", unsafe_allow_html=True)

    st.caption("💡 黄色のハイライトは重要な単語です")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("◀ 戻る"):
            st.session_state.sister_responses = None
            st.session_state.step = 5
            st.rerun()
    with col2:
        if st.button("Reading へ ▶", type="primary"):
            st.session_state.step = 7
            st.rerun()

# ===========================================
# STEP 7: Reading (Bilingual Display)
# ===========================================
elif st.session_state.step == 7:
    st.header("⑦ 英文を確認【Reading】")

    current_sister = st.session_state.current_sister
    response = st.session_state.sister_responses.get(current_sister, {})
    st.info(f"{SISTERS[current_sister]['emoji']} **{current_sister}** の返答")

    # English
    st.subheader("English:")
    st.success(response.get("response_en", ""))

    # Japanese
    st.subheader("日本語:")
    st.info(response.get("response_jp", ""))

    # Vocabulary
    words = response.get("words_to_highlight", [])
    if words:
        st.subheader("📚 Key Vocabulary:")
        for word in words:
            st.markdown(f"- **{word}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔊 もう一度聴く"):
            st.session_state.step = 6
            st.rerun()
    with col2:
        if st.button("Quiz へ ▶", type="primary"):
            st.session_state.step = 8
            st.rerun()

# ===========================================
# STEP 8: Quiz
# ===========================================
elif st.session_state.step == 8:
    st.header("⑧ 理解度チェック【Quiz】")

    with st.spinner("クイズを生成中..."):
        if st.session_state.quiz is None:
            try:
                current_sister = st.session_state.current_sister
                current_response = st.session_state.sister_responses.get(current_sister, {})
                kimi = get_kimi()
                quiz = kimi.generate_quiz(
                    current_response.get("response_en", "")
                )
                st.session_state.quiz = quiz
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.quiz = {
                    "question_en": "Did you understand?",
                    "question_jp": "理解できましたか？",
                    "options": [
                        {"text": "Yes, I understood", "correct": True},
                        {"text": "No, not really", "correct": False}
                    ],
                    "explanation_jp": ""
                }

    quiz = st.session_state.quiz

    st.subheader(f"❓ {quiz.get('question_en', '')}")
    st.caption(quiz.get('question_jp', ''))

    options = quiz.get("options", [])
    selected = st.radio(
        "Select your answer:",
        [opt.get("text", "") for opt in options],
        index=None
    )

    if selected:
        st.session_state.quiz_answer = selected
        correct_answer = next((opt for opt in options if opt.get("correct")), None)

        if correct_answer and selected == correct_answer.get("text"):
            st.success("✅ Correct!")
        else:
            st.error(f"❌ The correct answer was: {correct_answer.get('text', '') if correct_answer else 'Unknown'}")

        st.info(f"💡 {quiz.get('explanation_jp', '')}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("◀ 戻る"):
            st.session_state.quiz = None
            st.session_state.step = 7
            st.rerun()
    with col2:
        if st.button("Feedback へ ▶", type="primary", disabled=not selected):
            st.session_state.step = 9
            st.rerun()

# ===========================================
# STEP 9: Feedback & Next Guidance
# ===========================================
elif st.session_state.step == 9:
    st.header("⑨ 学習まとめ【Feedback】")

    st.subheader("📊 Today's Session:")

    # Writing feedback
    writing = st.session_state.writing_feedback
    if writing:
        st.markdown("**Writing:**")
        if writing.get("is_correct"):
            st.success(f"✅ Perfect! Rating: {'⭐' * writing.get('rating', 3)}")
        else:
            st.warning(f"📝 {len(writing.get('corrections', []))} corrections made")

    # Speaking feedback
    speaking = st.session_state.speaking_feedback
    if speaking:
        st.markdown("**Speaking:**")
        accuracy = speaking.get("accuracy_percent", 100)
        if accuracy >= 90:
            st.success(f"✅ Excellent! {accuracy}% accuracy")
        elif accuracy >= 70:
            st.warning(f"📝 Good effort! {accuracy}% accuracy")
        else:
            st.info(f"🎯 Keep practicing! {accuracy}% accuracy")

    # Quiz result
    st.markdown("**Comprehension:**")
    if st.session_state.quiz_answer:
        quiz = st.session_state.quiz
        correct = next((opt for opt in quiz.get("options", []) if opt.get("correct")), None)
        if correct and st.session_state.quiz_answer == correct.get("text"):
            st.success("✅ Quiz passed!")
        else:
            st.warning("📝 Review the listening section")

    st.divider()

    # Next steps
    st.subheader("🎯 Next Steps:")

    if speaking and speaking.get("focus_point_jp"):
        st.markdown(f"1. **発音**: {speaking.get('focus_point_jp')}")

    if writing and writing.get("corrections"):
        st.markdown("2. **文法**: Review the corrections from your writing")

    st.markdown("3. **練習**: Continue the conversation to build fluency!")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Topic", use_container_width=True):
            # Reset for new conversation
            for key in ["japanese_text", "english_text", "corrected_text",
                       "writing_feedback", "spoken_text", "speaking_feedback",
                       "sister_responses", "quiz", "quiz_answer", "audio_data"]:
                st.session_state[key] = "" if isinstance(st.session_state.get(key), str) else None
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("🔁 Continue Conversation", type="primary", use_container_width=True):
            # Save to history and continue
            current_sister = st.session_state.current_sister
            current_response = st.session_state.sister_responses.get(current_sister, {})
            st.session_state.conversation_history.append({
                "user": st.session_state.corrected_text,
                "sister": current_response.get("response_en", "")
            })
            # Reset for next turn but keep context
            st.session_state.japanese_text = ""
            st.session_state.english_text = ""
            st.session_state.corrected_text = ""
            st.session_state.writing_feedback = None
            st.session_state.spoken_text = ""
            st.session_state.speaking_feedback = None
            st.session_state.sister_responses = None
            st.session_state.quiz = None
            st.session_state.quiz_answer = None
            st.session_state.audio_data = None
            st.session_state.step = 1
            st.rerun()

# Footer
st.divider()
st.caption("Sisters-Multilingual-Coach v0.2.0 | 🎯 Goal: 英会話ができるようになる！")
