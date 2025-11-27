"""
Sisters-Multilingual-Coach - Complete Learning Flow
Goal: 英会話ができるようになる！
"""

import streamlit as st
import os
import json
import base64
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder

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
        "step": 0,  # 0 = placement test, 1-9 = learning flow
        "japanese_text": "",
        "english_text": "",
        "corrected_text": "",
        "writing_feedback": None,
        "spoken_text": "",
        "speaking_feedback": None,
        "sister_responses": None,
        "quiz": None,
        "quiz_answer": None,
        "current_sister": "Botan",
        "target_language": "English",
        "conversation_history": [],
        "audio_data": None,
        # Level assessment
        "cefr_level": None,  # A1, A2, B1, B2, C1, C2
        "level_info": None,  # Full level info dict
        "placement_test_phase": "intro",  # intro, grammar, vocabulary, listening, result
        "placement_answers": {},  # Store test answers
        "placement_questions": {},  # Store generated questions
        "sessions_completed": 0,
        "performance_history": [],  # Track performance for level adjustment
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

# CEFR Level colors
CEFR_COLORS = {
    "A1": "#4CAF50",  # Green - Beginner
    "A2": "#8BC34A",  # Light Green
    "B1": "#FFC107",  # Yellow - Intermediate
    "B2": "#FF9800",  # Orange
    "C1": "#F44336",  # Red - Advanced
    "C2": "#9C27B0",  # Purple - Mastery
}

# Sidebar
with st.sidebar:
    st.title("🌏 Settings")

    # Show CEFR Level if assessed
    if st.session_state.cefr_level:
        level = st.session_state.cefr_level
        level_info = st.session_state.level_info or {}
        color = CEFR_COLORS.get(level, "#666")
        st.markdown(f"""
        <div style="background-color: {color}; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px;">
            <span style="font-size: 24px; font-weight: bold; color: white;">CEFR {level}</span><br>
            <span style="color: white; font-size: 12px;">{level_info.get('level_name_jp', '')}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📊 レベル再測定", use_container_width=True):
            st.session_state.step = 0
            st.session_state.placement_test_phase = "intro"
            st.session_state.placement_answers = {}
            st.session_state.placement_questions = {}
            st.rerun()
        st.divider()

    st.subheader("Sister")
    for name, info in SISTERS.items():
        if st.button(
            f"{info['emoji']} {name}",
            use_container_width=True,
            type="primary" if st.session_state.current_sister == name else "secondary"
        ):
            st.session_state.current_sister = name
            st.session_state.audio_data = None
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
        current_sister = st.session_state.get("current_sister", "Botan")
        cefr_level = st.session_state.get("cefr_level")
        level_info = st.session_state.get("level_info")
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.current_sister = current_sister
        st.session_state.cefr_level = cefr_level
        st.session_state.level_info = level_info
        st.session_state.step = 1 if cefr_level else 0
        st.rerun()

# Main content
st.title(f"🌏 Sisters Multilingual Coach")
st.caption(f"🎯 Goal: 英会話ができるようになる！ | Partner: {SISTERS[st.session_state.current_sister]['emoji']} {st.session_state.current_sister}")

# ===========================================
# STEP 0: Placement Test
# ===========================================
if st.session_state.step == 0:
    phase = st.session_state.placement_test_phase

    # Intro phase
    if phase == "intro":
        st.header("📊 英語レベル診断テスト")
        st.markdown("""
        ### あなたの英語レベルを測定します

        **CEFR（ヨーロッパ言語共通参照枠）** に基づいて、あなたの英語力を判定します。

        | レベル | 説明 |
        |--------|------|
        | **A1** | 入門 - 基本的な表現を理解できる |
        | **A2** | 初級 - 日常的な表現を理解できる |
        | **B1** | 中級 - 要点を理解できる |
        | **B2** | 中上級 - 複雑な文章を理解できる |
        | **C1** | 上級 - 高度な内容を理解できる |
        | **C2** | 最上級 - ネイティブに近い |

        ---

        **テスト内容:**
        1. 文法問題 (5問)
        2. 語彙問題 (5問)
        3. リスニング問題 (3問)

        所要時間: 約5分
        """)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 テストを開始", type="primary", use_container_width=True):
                st.session_state.placement_test_phase = "grammar"
                st.session_state.placement_answers = {"grammar": [], "vocabulary": [], "listening": []}
                st.rerun()
        with col2:
            if st.button("⏭️ スキップ (A2で開始)", use_container_width=True):
                st.session_state.cefr_level = "A2"
                st.session_state.level_info = {
                    "level": "A2",
                    "level_name_en": "Elementary",
                    "level_name_jp": "初級",
                    "description_jp": "テストをスキップしました。A2レベルで開始します。"
                }
                st.session_state.step = 1
                st.rerun()

    # Grammar phase
    elif phase == "grammar":
        st.header("📝 文法テスト (1/3)")
        st.progress(0.33)

        # Generate questions if not already
        if "grammar" not in st.session_state.placement_questions:
            with st.spinner("問題を生成中..."):
                kimi = get_kimi()
                questions = kimi.generate_placement_test("grammar")
                st.session_state.placement_questions["grammar"] = questions.get("questions", [])

        questions = st.session_state.placement_questions.get("grammar", [])

        if questions:
            with st.form("grammar_form"):
                answers = []
                for i, q in enumerate(questions):
                    st.markdown(f"**Q{i+1}. ({q.get('level', '?')})** {q.get('question', '')}")
                    options = q.get("options", [])
                    answer = st.radio(
                        f"選択してください:",
                        options,
                        key=f"grammar_{i}",
                        index=None
                    )
                    answers.append(answer)
                    st.divider()

                if st.form_submit_button("次へ ▶", type="primary", use_container_width=True):
                    # Store answers with correctness
                    grammar_results = []
                    for i, (q, ans) in enumerate(zip(questions, answers)):
                        correct_idx = q.get("correct", 0)
                        options = q.get("options", [])
                        is_correct = ans == options[correct_idx] if ans and correct_idx < len(options) else False
                        grammar_results.append({
                            "level": q.get("level", "A1"),
                            "correct": is_correct
                        })
                    st.session_state.placement_answers["grammar"] = grammar_results
                    st.session_state.placement_test_phase = "vocabulary"
                    st.rerun()
        else:
            st.error("問題の生成に失敗しました")
            if st.button("再試行"):
                st.session_state.placement_questions.pop("grammar", None)
                st.rerun()

    # Vocabulary phase
    elif phase == "vocabulary":
        st.header("📚 語彙テスト (2/3)")
        st.progress(0.66)

        if "vocabulary" not in st.session_state.placement_questions:
            with st.spinner("問題を生成中..."):
                kimi = get_kimi()
                questions = kimi.generate_placement_test("vocabulary")
                st.session_state.placement_questions["vocabulary"] = questions.get("questions", [])

        questions = st.session_state.placement_questions.get("vocabulary", [])

        if questions:
            with st.form("vocabulary_form"):
                answers = []
                for i, q in enumerate(questions):
                    st.markdown(f"**Q{i+1}. ({q.get('level', '?')})** {q.get('question', '')}")
                    options = q.get("options", [])
                    answer = st.radio(
                        f"選択してください:",
                        options,
                        key=f"vocab_{i}",
                        index=None
                    )
                    answers.append(answer)
                    st.divider()

                if st.form_submit_button("次へ ▶", type="primary", use_container_width=True):
                    vocab_results = []
                    for i, (q, ans) in enumerate(zip(questions, answers)):
                        correct_idx = q.get("correct", 0)
                        options = q.get("options", [])
                        is_correct = ans == options[correct_idx] if ans and correct_idx < len(options) else False
                        vocab_results.append({
                            "level": q.get("level", "A1"),
                            "correct": is_correct
                        })
                    st.session_state.placement_answers["vocabulary"] = vocab_results
                    st.session_state.placement_test_phase = "listening"
                    st.rerun()
        else:
            st.error("問題の生成に失敗しました")
            if st.button("再試行"):
                st.session_state.placement_questions.pop("vocabulary", None)
                st.rerun()

    # Listening phase
    elif phase == "listening":
        st.header("🎧 リスニングテスト (3/3)")
        st.progress(1.0)

        if "listening" not in st.session_state.placement_questions:
            with st.spinner("問題を生成中..."):
                kimi = get_kimi()
                questions = kimi.generate_placement_test("listening")
                st.session_state.placement_questions["listening"] = questions.get("questions", [])

        questions = st.session_state.placement_questions.get("listening", [])

        if questions:
            with st.form("listening_form"):
                answers = []
                for i, q in enumerate(questions):
                    st.markdown(f"**Q{i+1}. ({q.get('level', '?')})**")

                    # Play audio
                    audio_text = q.get("audio_text", "")
                    if audio_text:
                        st.info(f"🔊 音声テキスト: \"{audio_text}\"")
                        # Generate TTS for listening
                        if st.session_state.get(f"listening_audio_{i}") is None:
                            try:
                                tts = get_tts()
                                audio_bytes = tts.generate_speech(audio_text, sister="Ojisan")
                                st.session_state[f"listening_audio_{i}"] = audio_bytes
                            except:
                                pass

                        if st.session_state.get(f"listening_audio_{i}"):
                            st.audio(st.session_state[f"listening_audio_{i}"], format="audio/mp3")

                    st.markdown(f"**{q.get('question', '')}**")
                    options = q.get("options", [])
                    answer = st.radio(
                        f"選択してください:",
                        options,
                        key=f"listen_{i}",
                        index=None
                    )
                    answers.append(answer)
                    st.divider()

                if st.form_submit_button("結果を見る 📊", type="primary", use_container_width=True):
                    listen_results = []
                    for i, (q, ans) in enumerate(zip(questions, answers)):
                        correct_idx = q.get("correct", 0)
                        options = q.get("options", [])
                        is_correct = ans == options[correct_idx] if ans and correct_idx < len(options) else False
                        listen_results.append({
                            "level": q.get("level", "A1"),
                            "correct": is_correct
                        })
                    st.session_state.placement_answers["listening"] = listen_results
                    st.session_state.placement_test_phase = "result"
                    st.rerun()
        else:
            st.error("問題の生成に失敗しました")
            if st.button("再試行"):
                st.session_state.placement_questions.pop("listening", None)
                st.rerun()

    # Result phase
    elif phase == "result":
        st.header("📊 診断結果")

        # Calculate results
        all_answers = st.session_state.placement_answers
        results_by_level = {"A1": 0, "A2": 0, "B1": 0, "B2": 0, "C1": 0}
        total_by_level = {"A1": 0, "A2": 0, "B1": 0, "B2": 0, "C1": 0}

        for category in ["grammar", "vocabulary", "listening"]:
            for ans in all_answers.get(category, []):
                level = ans.get("level", "A1")
                # Normalize level (A1-A2 -> A1 or A2)
                if "-" in level:
                    level = level.split("-")[0]
                if level in results_by_level:
                    total_by_level[level] += 1
                    if ans.get("correct"):
                        results_by_level[level] += 1

        with st.spinner("レベルを判定中..."):
            kimi = get_kimi()
            level_result = kimi.calculate_cefr_level({
                "results": results_by_level,
                "total": total_by_level,
                "raw_answers": all_answers
            })

        # Store level
        st.session_state.cefr_level = level_result.get("level", "A2")
        st.session_state.level_info = level_result

        # Display result
        level = level_result.get("level", "A2")
        color = CEFR_COLORS.get(level, "#666")

        st.markdown(f"""
        <div style="background-color: {color}; padding: 30px; border-radius: 20px; text-align: center; margin: 20px 0;">
            <span style="font-size: 48px; font-weight: bold; color: white;">CEFR {level}</span><br>
            <span style="color: white; font-size: 24px;">{level_result.get('level_name_jp', '')}</span><br>
            <span style="color: white; font-size: 14px;">{level_result.get('level_name_en', '')}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**📝 {level_result.get('description_jp', '')}**")

        # Show strengths and areas to improve
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ 強み")
            for strength in level_result.get("strengths_jp", []):
                st.markdown(f"- {strength}")

        with col2:
            st.subheader("📈 改善ポイント")
            for area in level_result.get("areas_to_improve_jp", []):
                st.markdown(f"- {area}")

        # Show score breakdown
        st.divider()
        st.subheader("📊 スコア詳細")
        col1, col2, col3 = st.columns(3)

        grammar_correct = sum(1 for a in all_answers.get("grammar", []) if a.get("correct"))
        vocab_correct = sum(1 for a in all_answers.get("vocabulary", []) if a.get("correct"))
        listen_correct = sum(1 for a in all_answers.get("listening", []) if a.get("correct"))

        with col1:
            st.metric("文法", f"{grammar_correct}/5")
        with col2:
            st.metric("語彙", f"{vocab_correct}/5")
        with col3:
            st.metric("リスニング", f"{listen_correct}/3")

        st.divider()

        if st.button("🚀 学習を開始する", type="primary", use_container_width=True):
            st.session_state.step = 1
            st.rerun()

# ===========================================
# STEP 1: Japanese Input
# ===========================================
elif st.session_state.step == 1:
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

    # Back button
    if st.button("◀ 戻る"):
        st.session_state.step = 3
        st.rerun()

    st.markdown("**マイクボタンを押して録音してください：**")
    st.caption("🔴 赤いボタンを押すと録音開始、もう一度押すと停止")

    # Audio recorder
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="3x",
        sample_rate=16000
    )

    # Show transcription result
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

        with st.spinner("音声を認識中..."):
            try:
                stt = get_stt()
                result = stt.transcribe_bytes(audio_bytes, filename="recording.wav", language="en")
                transcribed_text = result.get("text", "")

                if transcribed_text:
                    st.session_state.spoken_text = transcribed_text
                    st.success(f"**認識結果:** {transcribed_text}")

                    # Auto-proceed or manual button
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 録り直す", use_container_width=True):
                            st.session_state.spoken_text = ""
                            st.rerun()
                    with col2:
                        if st.button("発音チェックへ ▶", type="primary", use_container_width=True):
                            st.session_state.step = 5
                            st.rerun()
                else:
                    st.warning("音声を認識できませんでした。もう一度お試しください。")
            except Exception as e:
                st.error(f"STT Error: {e}")
                st.caption("音声認識に失敗しました。下のテキスト入力をお使いください。")

    # Fallback: Manual text input
    st.divider()
    with st.expander("💬 テキストで入力する（音声認識がうまくいかない場合）"):
        manual_text = st.text_input(
            "発音した内容を入力:",
            value=st.session_state.get("spoken_text", ""),
            placeholder="I want to go shopping tomorrow"
        )
        if st.button("この内容で発音チェック", use_container_width=True):
            if manual_text:
                st.session_state.spoken_text = manual_text
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

    # Calculate performance metrics
    writing = st.session_state.writing_feedback
    speaking = st.session_state.speaking_feedback
    quiz = st.session_state.quiz

    writing_score = writing.get("rating", 3) * 20 if writing else 0
    speaking_score = speaking.get("accuracy_percent", 0) if speaking else 0
    quiz_correct = False
    if st.session_state.quiz_answer and quiz:
        correct = next((opt for opt in quiz.get("options", []) if opt.get("correct")), None)
        quiz_correct = correct and st.session_state.quiz_answer == correct.get("text")
    quiz_score = 100 if quiz_correct else 0

    # Store performance for level tracking
    session_performance = {
        "writing_accuracy": writing_score,
        "speaking_accuracy": speaking_score,
        "quiz_correct_rate": quiz_score,
        "current_level": st.session_state.cefr_level or "A2",
        "sessions_completed": st.session_state.sessions_completed + 1
    }
    st.session_state.performance_history.append(session_performance)
    st.session_state.sessions_completed += 1

    st.subheader("📊 Today's Session:")

    # Show current level
    if st.session_state.cefr_level:
        level = st.session_state.cefr_level
        color = CEFR_COLORS.get(level, "#666")
        st.markdown(f"**現在のレベル:** <span style='background-color: {color}; color: white; padding: 2px 8px; border-radius: 4px;'>CEFR {level}</span>", unsafe_allow_html=True)

    # Writing feedback
    if writing:
        st.markdown("**Writing:**")
        if writing.get("is_correct"):
            st.success(f"✅ Perfect! Rating: {'⭐' * writing.get('rating', 3)}")
        else:
            st.warning(f"📝 {len(writing.get('corrections', []))} corrections made")

    # Speaking feedback
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
    if quiz_correct:
        st.success("✅ Quiz passed!")
    else:
        st.warning("📝 Review the listening section")

    # Level adjustment check (every 3 sessions)
    if st.session_state.sessions_completed >= 3 and st.session_state.sessions_completed % 3 == 0:
        st.divider()
        st.subheader("📈 レベル調整チェック")

        # Calculate average performance
        recent_sessions = st.session_state.performance_history[-3:]
        avg_writing = sum(s.get("writing_accuracy", 0) for s in recent_sessions) / 3
        avg_speaking = sum(s.get("speaking_accuracy", 0) for s in recent_sessions) / 3
        avg_quiz = sum(s.get("quiz_correct_rate", 0) for s in recent_sessions) / 3

        with st.spinner("パフォーマンスを分析中..."):
            try:
                kimi = get_kimi()
                analysis = kimi.analyze_performance({
                    "writing_accuracy": avg_writing,
                    "speaking_accuracy": avg_speaking,
                    "quiz_correct_rate": avg_quiz,
                    "current_level": st.session_state.cefr_level,
                    "sessions_completed": st.session_state.sessions_completed
                })

                if analysis.get("should_adjust") and analysis.get("confidence", 0) > 0.7:
                    new_level = analysis.get("recommended_level")
                    st.info(f"📊 **レベル調整の提案**: {st.session_state.cefr_level} → {new_level}")
                    st.caption(analysis.get("adjustment_reason_jp", ""))

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ {new_level}に変更", use_container_width=True):
                            st.session_state.cefr_level = new_level
                            st.session_state.level_info["level"] = new_level
                            st.success(f"レベルを{new_level}に更新しました！")
                            st.rerun()
                    with col2:
                        if st.button("⏭️ 現在のレベルを維持", use_container_width=True):
                            st.info("現在のレベルを維持します")
                else:
                    st.success("✅ 現在のレベルが適切です")
            except Exception as e:
                st.caption(f"レベル分析をスキップしました")

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
