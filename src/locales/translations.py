"""
Translations for Sisters-Multilingual-Coach
All localized strings are defined here.
"""

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
