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

# Initialize providers (cached for performance)
@st.cache_resource
def get_kimi():
    from llm import KimiLLM
    return KimiLLM()

@st.cache_resource
def get_tts():
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
        "native_text": "",  # Text in native language (was japanese_text)
        "target_text": "",  # Text in target language (was english_text)
        "corrected_text": "",
        "writing_feedback": None,
        "spoken_text": "",
        "speaking_feedback": None,
        "sister_responses": None,
        "quiz": None,
        "quiz_answer": None,
        "current_sister": "Botan",
        # Language settings
        "native_language": "日本語",  # User's native language
        "target_language": "English",  # Language being learned
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

    # Restore from URL params (survives iPhone sleep/reconnect)
    params = st.query_params

    # Language code to name mapping
    code_to_lang = {"en": "English", "ja": "日本語", "zh": "中文", "ko": "한국어", "es": "Español"}

    # Restore languages from code
    if "native" in params and params["native"] in code_to_lang:
        st.session_state.native_language = code_to_lang[params["native"]]
    if "target" in params and params["target"] in code_to_lang:
        st.session_state.target_language = code_to_lang[params["target"]]

    # Restore character
    if "char" in params and params["char"] in ["Botan", "Kasho", "Yuri", "Ojisan"]:
        st.session_state.current_sister = params["char"]

    # Restore CEFR level
    if "level" in params and not st.session_state.get("cefr_level"):
        level = params["level"]
        if level in ["A1", "A2", "B1", "B2", "C1", "C2"]:
            st.session_state.cefr_level = level
            st.session_state.level_info = {"level": level}
            st.session_state.placement_test_phase = "done"
            st.session_state.step = 1

init_session_state()

# Supported languages
LANGUAGES = {
    "English": {"code": "en", "flag": "🇺🇸", "native_name": "English"},
    "日本語": {"code": "ja", "flag": "🇯🇵", "native_name": "日本語"},
    "中文": {"code": "zh", "flag": "🇨🇳", "native_name": "中文"},
    "한국어": {"code": "ko", "flag": "🇰🇷", "native_name": "한국어"},
    "Español": {"code": "es", "flag": "🇪🇸", "native_name": "Español"},
}

# Goal text by target language, in each native language
GOALS = {
    "English": {
        "日本語": "英会話ができるようになる！",
        "English": "Become fluent in English!",
        "中文": "学会说英语！",
        "한국어": "영어를 잘하게 되자!",
        "Español": "¡Dominar el inglés!",
    },
    "日本語": {
        "日本語": "日本語が話せるようになる！",
        "English": "Become fluent in Japanese!",
        "中文": "学会说日语！",
        "한국어": "일본어를 잘하게 되자!",
        "Español": "¡Dominar el japonés!",
    },
    "中文": {
        "日本語": "中国語が話せるようになる！",
        "English": "Become fluent in Chinese!",
        "中文": "学会说中文！",
        "한국어": "중국어를 잘하게 되자!",
        "Español": "¡Dominar el chino!",
    },
    "한국어": {
        "日本語": "韓国語が話せるようになる！",
        "English": "Become fluent in Korean!",
        "中文": "学会说韩语！",
        "한국어": "한국어를 잘하게 되자!",
        "Español": "¡Dominar el coreano!",
    },
    "Español": {
        "日本語": "スペイン語が話せるようになる！",
        "English": "Become fluent in Spanish!",
        "中文": "学会说西班牙语！",
        "한국어": "스페인어를 잘하게 되자!",
        "Español": "¡Dominar el español!",
    },
}

def get_goal_text():
    """Get goal text in user's native language for their target language"""
    target = st.session_state.get("target_language", "English")
    native = st.session_state.get("native_language", "日本語")
    return GOALS.get(target, {}).get(native, GOALS["English"]["日本語"])

# UI text translations
UI_TEXT = {
    "English": {
        "what_to_say": "What do you want to say?",
        "write_in_target": "Write it in {target}",
        "placeholder_native": "Example: I want to go shopping tomorrow",
        "next": "Next ▶",
        "back": "◀ Back",
        "correction": "Correction",
        "your_writing": "Your writing:",
        "corrected": "Corrected:",
        "speaking_practice": "Read this aloud",
        "listen_example": "🔊 Listen to example",
        "your_turn": "🎤 Your turn",
        "record_instruction": "Press the microphone button to record:",
        # Placement test
        "placement_title": "📊 {target} Level Assessment",
        "placement_intro": "### Assess your {target} level\n\nWe'll determine your level based on **CEFR (Common European Framework)**.",
        "cefr_table": """
| Level | Description |
|-------|-------------|
| **A1** | Beginner - Can understand basic expressions |
| **A2** | Elementary - Can understand everyday expressions |
| **B1** | Intermediate - Can understand main points |
| **B2** | Upper-Intermediate - Can understand complex texts |
| **C1** | Advanced - Can understand demanding content |
| **C2** | Mastery - Near-native proficiency |
""",
        "test_content": "**Test content:**\n1. Grammar (5 questions)\n2. Vocabulary (5 questions)\n3. Listening (3 questions)\n\nTime: ~5 minutes",
        "start_test": "📝 Start Test",
        "retake_test": "📊 Retake Level Test",
        "skip_test": "⏭️ Skip (Start at A2)",
        "grammar_test": "📝 Grammar Test (1/3)",
        "vocab_test": "📚 Vocabulary Test (2/3)",
        "listening_test": "🎧 Listening Test (3/3)",
        "select_answer": "Select your answer:",
        "generating": "Generating questions...",
        "see_results": "See Results 📊",
        "result_title": "📊 Assessment Results",
        "strengths": "✅ Strengths",
        "improve": "📈 Areas to Improve",
        "score_detail": "📊 Score Details",
        "start_learning": "🚀 Start Learning",
        "skip_desc": "Test skipped. Starting at A2 level.",
        "progress_steps": ["1.Native", "2.Writing", "3.Correction", "4.Speaking", "5.Pronunciation", "6.Listening", "7.Reading", "8.Quiz", "9.Feedback"],
    },
    "日本語": {
        "what_to_say": "何を言いたいですか？",
        "write_in_target": "{target}で書いてください",
        "placeholder_native": "例: 明日、買い物に行きたいな",
        "next": "次へ ▶",
        "back": "◀ 戻る",
        "correction": "添削",
        "your_writing": "あなたの文章:",
        "corrected": "添削後:",
        "speaking_practice": "声に出して読んでください",
        "listen_example": "🔊 お手本を聴く",
        "your_turn": "🎤 あなたの番です",
        "record_instruction": "マイクボタンを押して録音してください：",
        # Placement test
        "placement_title": "📊 {target}レベル診断テスト",
        "placement_intro": "### あなたの{target}レベルを測定します\n\n**CEFR（ヨーロッパ言語共通参照枠）** に基づいて判定します。",
        "cefr_table": """
| レベル | 説明 |
|--------|------|
| **A1** | 入門 - 基本的な表現を理解できる |
| **A2** | 初級 - 日常的な表現を理解できる |
| **B1** | 中級 - 要点を理解できる |
| **B2** | 中上級 - 複雑な文章を理解できる |
| **C1** | 上級 - 高度な内容を理解できる |
| **C2** | 最上級 - ネイティブに近い |
""",
        "test_content": "**テスト内容:**\n1. 文法問題 (5問)\n2. 語彙問題 (5問)\n3. リスニング問題 (3問)\n\n所要時間: 約5分",
        "start_test": "📝 テストを開始",
        "retake_test": "📊 レベル再測定",
        "skip_test": "⏭️ スキップ (A2で開始)",
        "grammar_test": "📝 文法テスト (1/3)",
        "vocab_test": "📚 語彙テスト (2/3)",
        "listening_test": "🎧 リスニングテスト (3/3)",
        "select_answer": "選択してください:",
        "generating": "問題を生成中...",
        "see_results": "結果を見る 📊",
        "result_title": "📊 診断結果",
        "strengths": "✅ 強み",
        "improve": "📈 改善ポイント",
        "score_detail": "📊 スコア詳細",
        "start_learning": "🚀 学習を開始する",
        "skip_desc": "テストをスキップしました。A2レベルで開始します。",
        "progress_steps": ["1.日本語", "2.Writing", "3.添削", "4.Speaking", "5.発音添削", "6.Listening", "7.Reading", "8.Quiz", "9.Feedback"],
    },
    "中文": {
        "what_to_say": "你想说什么？",
        "write_in_target": "用{target}写",
        "placeholder_native": "例如：我明天想去购物",
        "next": "下一步 ▶",
        "back": "◀ 返回",
        "correction": "修改",
        "your_writing": "你的文章:",
        "corrected": "修改后:",
        "speaking_practice": "请大声朗读",
        "listen_example": "🔊 听示范",
        "your_turn": "🎤 轮到你了",
        "record_instruction": "按麦克风按钮录音：",
        # Placement test
        "placement_title": "📊 {target}水平测试",
        "placement_intro": "### 测试你的{target}水平\n\n我们将根据 **CEFR（欧洲语言共同参考框架）** 来评估你的水平。",
        "cefr_table": """
| 级别 | 描述 |
|------|------|
| **A1** | 入门 - 能理解基本表达 |
| **A2** | 初级 - 能理解日常表达 |
| **B1** | 中级 - 能理解要点 |
| **B2** | 中高级 - 能理解复杂文章 |
| **C1** | 高级 - 能理解高难度内容 |
| **C2** | 精通 - 接近母语水平 |
""",
        "test_content": "**测试内容:**\n1. 语法 (5题)\n2. 词汇 (5题)\n3. 听力 (3题)\n\n时间: 约5分钟",
        "start_test": "📝 开始测试",
        "retake_test": "📊 重新测试等级",
        "skip_test": "⏭️ 跳过 (从A2开始)",
        "grammar_test": "📝 语法测试 (1/3)",
        "vocab_test": "📚 词汇测试 (2/3)",
        "listening_test": "🎧 听力测试 (3/3)",
        "select_answer": "请选择:",
        "generating": "生成题目中...",
        "see_results": "查看结果 📊",
        "result_title": "📊 测试结果",
        "strengths": "✅ 优势",
        "improve": "📈 需要改进",
        "score_detail": "📊 分数详情",
        "start_learning": "🚀 开始学习",
        "skip_desc": "已跳过测试。从A2级别开始。",
        "progress_steps": ["1.母语", "2.写作", "3.修改", "4.口语", "5.发音", "6.听力", "7.阅读", "8.测验", "9.反馈"],
    },
    "한국어": {
        "what_to_say": "무엇을 말하고 싶으세요?",
        "write_in_target": "{target}로 쓰세요",
        "placeholder_native": "예: 내일 쇼핑하러 가고 싶어",
        "next": "다음 ▶",
        "back": "◀ 뒤로",
        "correction": "수정",
        "your_writing": "당신의 글:",
        "corrected": "수정 후:",
        "speaking_practice": "소리 내어 읽어주세요",
        "listen_example": "🔊 예시 듣기",
        "your_turn": "🎤 당신 차례입니다",
        "record_instruction": "마이크 버튼을 눌러 녹음하세요:",
        # Placement test
        "placement_title": "📊 {target} 레벨 테스트",
        "placement_intro": "### {target} 레벨을 측정합니다\n\n**CEFR(유럽공통언어표준)** 기준으로 평가합니다.",
        "cefr_table": """
| 레벨 | 설명 |
|------|------|
| **A1** | 입문 - 기본 표현을 이해할 수 있음 |
| **A2** | 초급 - 일상 표현을 이해할 수 있음 |
| **B1** | 중급 - 요점을 이해할 수 있음 |
| **B2** | 중상급 - 복잡한 글을 이해할 수 있음 |
| **C1** | 고급 - 어려운 내용을 이해할 수 있음 |
| **C2** | 최상급 - 원어민 수준 |
""",
        "test_content": "**테스트 내용:**\n1. 문법 (5문제)\n2. 어휘 (5문제)\n3. 듣기 (3문제)\n\n소요시간: 약 5분",
        "start_test": "📝 테스트 시작",
        "retake_test": "📊 레벨 재측정",
        "skip_test": "⏭️ 건너뛰기 (A2로 시작)",
        "grammar_test": "📝 문법 테스트 (1/3)",
        "vocab_test": "📚 어휘 테스트 (2/3)",
        "listening_test": "🎧 듣기 테스트 (3/3)",
        "select_answer": "선택하세요:",
        "generating": "문제 생성 중...",
        "see_results": "결과 보기 📊",
        "result_title": "📊 테스트 결과",
        "strengths": "✅ 강점",
        "improve": "📈 개선점",
        "score_detail": "📊 점수 상세",
        "start_learning": "🚀 학습 시작",
        "skip_desc": "테스트를 건너뛰었습니다. A2 레벨로 시작합니다.",
        "progress_steps": ["1.모국어", "2.작문", "3.수정", "4.말하기", "5.발음", "6.듣기", "7.읽기", "8.퀴즈", "9.피드백"],
    },
    "Español": {
        "what_to_say": "¿Qué quieres decir?",
        "write_in_target": "Escríbelo en {target}",
        "placeholder_native": "Ejemplo: Quiero ir de compras mañana",
        "next": "Siguiente ▶",
        "back": "◀ Atrás",
        "correction": "Corrección",
        "your_writing": "Tu texto:",
        "corrected": "Corregido:",
        "speaking_practice": "Léelo en voz alta",
        "listen_example": "🔊 Escuchar ejemplo",
        "your_turn": "🎤 Tu turno",
        "record_instruction": "Presiona el botón del micrófono para grabar:",
        # Placement test
        "placement_title": "📊 Prueba de nivel de {target}",
        "placement_intro": "### Evaluamos tu nivel de {target}\n\nBasado en **MCER (Marco Común Europeo de Referencia)**.",
        "cefr_table": """
| Nivel | Descripción |
|-------|-------------|
| **A1** | Principiante - Comprende expresiones básicas |
| **A2** | Elemental - Comprende expresiones cotidianas |
| **B1** | Intermedio - Comprende los puntos principales |
| **B2** | Intermedio alto - Comprende textos complejos |
| **C1** | Avanzado - Comprende contenido exigente |
| **C2** | Maestría - Nivel casi nativo |
""",
        "test_content": "**Contenido:**\n1. Gramática (5 preguntas)\n2. Vocabulario (5 preguntas)\n3. Comprensión auditiva (3 preguntas)\n\nTiempo: ~5 minutos",
        "start_test": "📝 Iniciar prueba",
        "retake_test": "📊 Repetir prueba de nivel",
        "skip_test": "⏭️ Omitir (Empezar en A2)",
        "grammar_test": "📝 Prueba de gramática (1/3)",
        "vocab_test": "📚 Prueba de vocabulario (2/3)",
        "listening_test": "🎧 Prueba de comprensión auditiva (3/3)",
        "select_answer": "Selecciona tu respuesta:",
        "generating": "Generando preguntas...",
        "see_results": "Ver resultados 📊",
        "result_title": "📊 Resultados",
        "strengths": "✅ Fortalezas",
        "improve": "📈 Áreas a mejorar",
        "score_detail": "📊 Detalle de puntuación",
        "start_learning": "🚀 Comenzar a aprender",
        "skip_desc": "Prueba omitida. Comenzando en nivel A2.",
        "progress_steps": ["1.Nativo", "2.Escritura", "3.Corrección", "4.Hablar", "5.Pronunciación", "6.Escuchar", "7.Lectura", "8.Quiz", "9.Feedback"],
    },
}

def get_ui_text(key: str):
    """Get UI text in user's native language"""
    native = st.session_state.get("native_language", "日本語")
    texts = UI_TEXT.get(native, UI_TEXT["English"])
    text = texts.get(key, key)
    # Replace {target} placeholder if present (only for strings)
    if isinstance(text, str) and "{target}" in text:
        text = text.format(target=st.session_state.get("target_language", "English"))
    return text

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

    # Language Selection
    st.subheader("🗣️ Languages")

    col1, col2 = st.columns(2)
    with col1:
        native_options = list(LANGUAGES.keys())
        native_idx = native_options.index(st.session_state.native_language) if st.session_state.native_language in native_options else 1
        new_native = st.selectbox(
            "Native",
            native_options,
            index=native_idx,
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x}"
        )
        if new_native != st.session_state.native_language:
            st.session_state.native_language = new_native
            st.query_params["native"] = LANGUAGES[new_native]["code"]
            st.rerun()

    with col2:
        # Filter out native language from target options
        target_options = [lang for lang in LANGUAGES.keys() if lang != st.session_state.native_language]
        target_idx = target_options.index(st.session_state.target_language) if st.session_state.target_language in target_options else 0
        new_target = st.selectbox(
            "Learning",
            target_options,
            index=target_idx,
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x}"
        )
        if new_target != st.session_state.target_language:
            st.session_state.target_language = new_target
            st.query_params["target"] = LANGUAGES[new_target]["code"]
            st.rerun()

    st.caption(f"{LANGUAGES[st.session_state.native_language]['flag']} → {LANGUAGES[st.session_state.target_language]['flag']}")
    st.divider()

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
        if st.button(get_ui_text("retake_test"), use_container_width=True):
            st.session_state.step = 0
            st.session_state.placement_test_phase = "intro"
            st.session_state.placement_answers = {}
            st.session_state.placement_questions = {}
            st.rerun()
        st.divider()

    st.subheader("Characters")
    for name, info in SISTERS.items():
        if st.button(
            f"{info['emoji']} {name}",
            use_container_width=True,
            type="primary" if st.session_state.current_sister == name else "secondary"
        ):
            st.session_state.current_sister = name
            st.session_state.audio_data = None
            st.query_params["char"] = name
            st.rerun()

    st.caption(f"Best for: {SISTERS[st.session_state.current_sister]['desc']}")

    st.divider()

    st.subheader("Progress")
    steps = get_ui_text("progress_steps")
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
        recorder_id = st.session_state.get("recorder_id", 0) + 1
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.current_sister = current_sister
        st.session_state.cefr_level = cefr_level
        st.session_state.level_info = level_info
        st.session_state.recorder_id = recorder_id
        st.session_state.step = 1 if cefr_level else 0
        st.rerun()

# Main content
st.title(f"🌏 Sisters Multilingual Coach")
st.caption(f"🎯 Goal: {get_goal_text()} | Partner: {SISTERS[st.session_state.current_sister]['emoji']} {st.session_state.current_sister}")

# ===========================================
# STEP 0: Placement Test
# ===========================================
if st.session_state.step == 0:
    # If already assessed, skip to step 1
    if st.session_state.cefr_level and st.session_state.placement_test_phase == "done":
        st.session_state.step = 1
        st.rerun()

    phase = st.session_state.placement_test_phase

    # Intro phase
    if phase == "intro":
        target_lang = st.session_state.target_language
        st.header(get_ui_text("placement_title"))
        st.markdown(get_ui_text("placement_intro"))
        st.markdown(get_ui_text("cefr_table"))
        st.markdown("---")
        st.markdown(get_ui_text("test_content"))

        col1, col2 = st.columns(2)
        with col1:
            if st.button(get_ui_text("start_test"), type="primary", use_container_width=True):
                st.session_state.placement_test_phase = "grammar"
                st.session_state.placement_answers = {"grammar": [], "vocabulary": [], "listening": []}
                st.rerun()
        with col2:
            if st.button(get_ui_text("skip_test"), use_container_width=True):
                st.session_state.cefr_level = "A2"
                st.session_state.level_info = {
                    "level": "A2",
                    "level_name_en": "Elementary",
                    "level_name_jp": "初級",
                    "description": get_ui_text("skip_desc")
                }
                st.session_state.placement_test_phase = "done"
                st.session_state.step = 1
                st.query_params["level"] = "A2"  # Save to URL for iPhone sleep recovery
                st.rerun()

    # Grammar phase
    elif phase == "grammar":
        st.header(get_ui_text("grammar_test"))
        st.progress(0.33)

        # Generate questions if not already
        if "grammar" not in st.session_state.placement_questions:
            with st.spinner(get_ui_text("generating")):
                kimi = get_kimi()
                questions = kimi.generate_placement_test("grammar", st.session_state.target_language)
                st.session_state.placement_questions["grammar"] = questions.get("questions", [])

        questions = st.session_state.placement_questions.get("grammar", [])

        if questions:
            with st.form("grammar_form"):
                answers = []
                for i, q in enumerate(questions):
                    st.markdown(f"**Q{i+1}. ({q.get('level', '?')})** {q.get('question', '')}")
                    options = q.get("options", [])
                    answer = st.radio(
                        get_ui_text("select_answer"),
                        options,
                        key=f"grammar_{i}",
                        index=None
                    )
                    answers.append(answer)
                    st.divider()

                if st.form_submit_button(get_ui_text("next"), type="primary", use_container_width=True):
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
        st.header(get_ui_text("vocab_test"))
        st.progress(0.66)

        if "vocabulary" not in st.session_state.placement_questions:
            with st.spinner(get_ui_text("generating")):
                kimi = get_kimi()
                questions = kimi.generate_placement_test("vocabulary", st.session_state.target_language)
                st.session_state.placement_questions["vocabulary"] = questions.get("questions", [])

        questions = st.session_state.placement_questions.get("vocabulary", [])

        if questions:
            with st.form("vocabulary_form"):
                answers = []
                for i, q in enumerate(questions):
                    st.markdown(f"**Q{i+1}. ({q.get('level', '?')})** {q.get('question', '')}")
                    options = q.get("options", [])
                    answer = st.radio(
                        get_ui_text("select_answer"),
                        options,
                        key=f"vocab_{i}",
                        index=None
                    )
                    answers.append(answer)
                    st.divider()

                if st.form_submit_button(get_ui_text("next"), type="primary", use_container_width=True):
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
        st.header(get_ui_text("listening_test"))
        st.progress(1.0)

        if "listening" not in st.session_state.placement_questions:
            with st.spinner(get_ui_text("generating")):
                kimi = get_kimi()
                questions = kimi.generate_placement_test("listening", st.session_state.target_language)
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
                        st.info(f"🔊 \"{audio_text}\"")
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
                        get_ui_text("select_answer"),
                        options,
                        key=f"listen_{i}",
                        index=None
                    )
                    answers.append(answer)
                    st.divider()

                if st.form_submit_button(get_ui_text("see_results"), type="primary", use_container_width=True):
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
        level = level_result.get("level", "A2")
        st.session_state.cefr_level = level
        st.session_state.level_info = level_result
        st.query_params["level"] = level  # Save to URL for iPhone sleep recovery

        # Display result
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
            st.session_state.placement_test_phase = "done"
            st.session_state.step = 1
            st.rerun()

# ===========================================
# STEP 1: Native Language Input
# ===========================================
elif st.session_state.step == 1:
    native_lang = st.session_state.native_language
    target_lang = st.session_state.target_language
    native_flag = LANGUAGES[native_lang]["flag"]

    st.header(f"① {native_flag} {get_ui_text('what_to_say')}")
    st.caption("💡 Ctrl+Enter")

    with st.form("step1_form"):
        native_input = st.text_area(
            get_ui_text("what_to_say"),
            value=st.session_state.native_text,
            placeholder=get_ui_text("placeholder_native"),
            height=100
        )
        submitted = st.form_submit_button(get_ui_text("next"), type="primary")

        if submitted and native_input:
            st.session_state.native_text = native_input
            st.session_state.step = 2
            st.rerun()

# ===========================================
# STEP 2: Target Language Writing
# ===========================================
elif st.session_state.step == 2:
    native_lang = st.session_state.native_language
    target_lang = st.session_state.target_language
    target_flag = LANGUAGES[target_lang]["flag"]

    st.header(f"② {target_flag} {get_ui_text('write_in_target')}【Writing】")
    st.caption("💡 Ctrl+Enter")

    st.info(f"💬 {st.session_state.native_text}")

    # Back button outside form
    if st.button(get_ui_text("back")):
        st.session_state.step = 1
        st.rerun()

    with st.form("step2_form"):
        target_input = st.text_area(
            get_ui_text("write_in_target"),
            value=st.session_state.target_text,
            placeholder="",
            height=100
        )
        submitted = st.form_submit_button(f"{get_ui_text('correction')} ✓", type="primary", use_container_width=True)

        if submitted and target_input:
            st.session_state.target_text = target_input
            st.session_state.step = 3
            st.rerun()

# ===========================================
# STEP 3: Writing Correction
# ===========================================
elif st.session_state.step == 3:
    native_lang = st.session_state.native_language
    target_lang = st.session_state.target_language

    st.header(f"③ {get_ui_text('correction')}")

    with st.spinner("..."):
        if st.session_state.writing_feedback is None:
            try:
                kimi = get_kimi()
                feedback = kimi.correct_writing(
                    st.session_state.native_text,
                    st.session_state.target_text,
                    native_lang,
                    target_lang
                )
                st.session_state.writing_feedback = feedback
                st.session_state.corrected_text = feedback.get("corrected", st.session_state.target_text)
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.writing_feedback = {
                    "original": st.session_state.target_text,
                    "corrected": st.session_state.target_text,
                    "is_correct": True,
                    "corrections": [],
                    "rating": 3,
                    "encouragement": "Service unavailable"
                }
                st.session_state.corrected_text = st.session_state.target_text

    feedback = st.session_state.writing_feedback

    # Show results
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(get_ui_text("your_writing"))
        st.info(feedback.get("original", st.session_state.target_text))

    with col2:
        st.subheader(get_ui_text("corrected"))
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
            st.caption(f"  💡 {c.get('explanation', '')}")

    # Rating
    rating = feedback.get("rating", 3)
    st.markdown(f"**Rating:** {'⭐' * rating}")
    st.info(f"💪 {feedback.get('encouragement', 'Keep going!')}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_ui_text("back")):
            st.session_state.writing_feedback = None
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button(get_ui_text("next"), type="primary"):
            st.session_state.step = 4
            st.rerun()

# ===========================================
# STEP 4: Speaking Practice
# ===========================================
elif st.session_state.step == 4:
    target_lang = st.session_state.target_language
    target_code = LANGUAGES[target_lang]["code"]

    st.header(f"④ {get_ui_text('speaking_practice')}【Speaking】")

    st.success(f"📖 {get_ui_text('speaking_practice')}: **{st.session_state.corrected_text}**")

    # Back button at top
    if st.button(get_ui_text("back"), key="step4_back_btn"):
        st.session_state.step = 3
        st.rerun()

    # Two columns: Example (left) and Recording (right)
    col_example, col_record = st.columns(2)

    with col_example:
        st.subheader(get_ui_text("listen_example"))
        if st.button("▶ Play Example", key="play_example_btn", use_container_width=True):
            try:
                tts = get_tts()
                example_audio = tts.generate_speech(
                    st.session_state.corrected_text,
                    sister="User"  # Use Sam (male) voice for example
                )
                st.session_state.example_audio = example_audio
            except Exception as e:
                st.error(f"TTS Error: {e}")
        if st.session_state.get("example_audio"):
            st.audio(st.session_state.example_audio, format="audio/mp3")

    with col_record:
        st.subheader(get_ui_text("your_turn"))
        st.markdown(f"**{get_ui_text('record_instruction')}**")

        # Audio recorder (only show if no recording yet)
        if not st.session_state.get("recorded_audio") and not st.session_state.get("spoken_text"):
            from audio_recorder_streamlit import audio_recorder
            # Use dynamic key to prevent cache issues on retry
            recorder_key = f"audio_recorder_{st.session_state.get('recorder_id', 0)}"
            recorded_audio = audio_recorder(
                text="",
                recording_color="#e74c3c",
                neutral_color="#3498db",
                icon_name="microphone",
                icon_size="2x",
                sample_rate=16000,
                key=recorder_key
            )
            # Save recording to session state for preview
            if recorded_audio:
                st.session_state.recorded_audio = recorded_audio
                st.rerun()

    # Preview recorded audio before processing
    if st.session_state.get("recorded_audio") and not st.session_state.get("spoken_text"):
        st.audio(st.session_state.recorded_audio, format="audio/wav")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 録り直す", key="rerecord_btn", use_container_width=True):
                st.session_state.recorded_audio = None
                st.session_state.example_audio = None
                st.session_state.recorder_id = st.session_state.get("recorder_id", 0) + 1
                st.rerun()
        with col_b:
            if st.button("✅ 認識する", key="recognize_btn", type="primary", use_container_width=True):
                with st.spinner("認識中..."):
                    try:
                        stt = get_stt()
                        result = stt.transcribe_bytes(st.session_state.recorded_audio, filename="recording.wav", language=target_code)
                        transcribed_text = result.get("text", "")
                        if transcribed_text:
                            st.session_state.spoken_text = transcribed_text
                            st.rerun()
                        else:
                            st.warning("音声を認識できませんでした。")
                            st.session_state.recorded_audio = None
                            st.rerun()
                    except Exception as e:
                        st.error(f"STT Error: {e}")

    # Show result and buttons (outside columns, full width)
    if st.session_state.get("spoken_text"):
        st.success(f"**認識結果:** {st.session_state.spoken_text}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 録り直す", key="retry_btn", use_container_width=True):
                st.session_state.spoken_text = ""
                st.session_state.recorded_audio = None
                st.session_state.example_audio = None
                st.session_state.recorder_id = st.session_state.get("recorder_id", 0) + 1
                st.rerun()
        with col2:
            if st.button("発音チェックへ ▶", key="proceed_btn", type="primary", use_container_width=True):
                st.session_state.step = 5
                st.rerun()

    # Fallback: Manual text input
    st.divider()
    with st.expander("💬 テキストで入力する（音声認識がうまくいかない場合）"):
        manual_text = st.text_input(
            "発音した内容を入力:",
            value=st.session_state.get("spoken_text", ""),
            placeholder="I want to go shopping tomorrow",
            key="manual_text_input"
        )
        if st.button("この内容で発音チェック", key="manual_proceed_btn", use_container_width=True):
            if manual_text:
                st.session_state.spoken_text = manual_text
                st.session_state.step = 5
                st.rerun()

# ===========================================
# STEP 5: Speaking Correction
# ===========================================
elif st.session_state.step == 5:
    native_lang = st.session_state.native_language
    target_lang = st.session_state.target_language

    st.header("⑤ Speaking Feedback")

    with st.spinner("..."):
        if st.session_state.speaking_feedback is None:
            try:
                kimi = get_kimi()
                feedback = kimi.correct_speaking(
                    st.session_state.corrected_text,
                    st.session_state.spoken_text,
                    native_lang,
                    target_lang
                )
                st.session_state.speaking_feedback = feedback
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.speaking_feedback = {
                    "target": st.session_state.corrected_text,
                    "spoken": st.session_state.spoken_text,
                    "accuracy_percent": 100,
                    "word_comparison": [],
                    "overall_feedback": "Could not analyze",
                    "focus_point": "Please try again"
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
            if not w.get("correct") and w.get("tip"):
                st.caption(f"  💡 {w.get('tip', '')}")

    # Overall feedback
    st.info(f"📊 {feedback.get('overall_feedback', '')}")
    st.warning(f"🎯 {feedback.get('focus_point', '')}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(get_ui_text("back")):
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
    native_lang = st.session_state.native_language
    target_lang = st.session_state.target_language

    st.header(f"⑥ Listening")
    st.caption(f"💡 Switch characters in sidebar")

    # Initialize sister_responses if needed
    if st.session_state.sister_responses is None:
        st.session_state.sister_responses = {}

    # Generate response ONLY for current sister (lazy loading - 4x faster)
    current_sister = st.session_state.current_sister
    if current_sister not in st.session_state.sister_responses:
        with st.spinner("..."):
            try:
                kimi = get_kimi()
                response = kimi.sister_response(
                    current_sister,
                    st.session_state.corrected_text,
                    st.session_state.conversation_history,
                    target_lang,
                    native_lang
                )
                st.session_state.sister_responses[current_sister] = response
            except Exception as e:
                st.error(f"{current_sister} Error: {e}")
                st.session_state.sister_responses[current_sister] = {
                    "response_en": f"That sounds interesting! Tell me more.",
                    "response_jp": "Interesting!",
                    "words_to_highlight": ["interesting", "more"]
                }

    response = st.session_state.sister_responses.get(current_sister, {})
    response_en = response.get("response_en", "")

    # Show current sister indicator
    st.success(f"{SISTERS[current_sister]['emoji']} **{current_sister}** の返答")

    # Display with word highlighting
    st.subheader("🔊 Listen:")

    # TTS Playback
    if st.button("▶ Play", key="step6_play_btn"):
        try:
            tts = get_tts()
            audio_bytes = tts.generate_speech(response_en, sister=current_sister)
            st.session_state.audio_data = audio_bytes
        except Exception as e:
            st.error(f"TTS Error: {e}")

    if st.session_state.get("audio_data"):
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
        if st.button("◀ 戻る", key="step6_back_btn"):
            st.session_state.sister_responses = None
            st.session_state.step = 5
            st.rerun()
    with col2:
        if st.button("Reading へ ▶", key="step6_next_btn", type="primary"):
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

    # Store performance for level tracking (only once per session)
    if not st.session_state.get("_feedback_recorded"):
        session_performance = {
            "writing_accuracy": writing_score,
            "speaking_accuracy": speaking_score,
            "quiz_correct_rate": quiz_score,
            "current_level": st.session_state.cefr_level or "A2",
            "sessions_completed": st.session_state.sessions_completed + 1
        }
        st.session_state.performance_history.append(session_performance)
        st.session_state.sessions_completed += 1
        st.session_state._feedback_recorded = True

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
            for key in ["native_text", "target_text", "corrected_text",
                       "writing_feedback", "spoken_text", "speaking_feedback",
                       "sister_responses", "quiz", "quiz_answer", "audio_data",
                       "_feedback_recorded", "recorded_audio", "example_audio"]:
                st.session_state[key] = "" if isinstance(st.session_state.get(key), str) else None
            st.session_state.recorder_id = st.session_state.get("recorder_id", 0) + 1
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
            st.session_state.native_text = ""
            st.session_state.target_text = ""
            st.session_state.corrected_text = ""
            st.session_state.writing_feedback = None
            st.session_state.spoken_text = ""
            st.session_state.speaking_feedback = None
            st.session_state.sister_responses = None
            st.session_state.quiz = None
            st.session_state.quiz_answer = None
            st.session_state.audio_data = None
            st.session_state._feedback_recorded = None
            st.session_state.recorded_audio = None
            st.session_state.example_audio = None
            st.session_state.recorder_id = st.session_state.get("recorder_id", 0) + 1
            st.session_state.step = 1
            st.rerun()

# Footer
st.divider()
st.caption(f"Sisters-Multilingual-Coach v0.2.0 | 🎯 Goal: {get_goal_text()}")
