"""
日本語翻訳 - Sisters-Multilingual-Coach
"""

LANGUAGE_INFO = {
    "code": "ja",
    "flag": "🇯🇵",
    "native_name": "日本語"
}

# 各ターゲット言語のゴールテキスト（日本語話者向け）
GOALS = {
    "English": "英会話ができるようになる！",
    "日本語": "日本語が話せるようになる！",
    "中文": "中国語が話せるようになる！",
    "한국어": "韓国語が話せるようになる！",
    "Español": "スペイン語が話せるようになる！",
}

# UI テキスト
UI_TEXT = {
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
    # モード選択
    "mode_title": "モード",
    "mode_speaking": "発信",
    "mode_listening": "受信",
    "mode_speaking_help": "あなたから話しかける",
    "mode_listening_help": "キャラから話しかけられる",
    "mode_caption": "📤 自分から話す | 📥 相手から話される",
    # リスニングモード
    "listen_to_character": "{character}の話を聴く",
    "what_did_they_say": "何と言いましたか？",
    "your_response": "あなたの返答",
    "write_response": "{target}で返答を書いてください",
    # レベル診断テスト
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
    # CEFRレベル名
    "cefr_levels": {
        "A1": "入門",
        "A2": "初級",
        "B1": "中級",
        "B2": "中上級",
        "C1": "上級",
        "C2": "最上級",
    },
}
