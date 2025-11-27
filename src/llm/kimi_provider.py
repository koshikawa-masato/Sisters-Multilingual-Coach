"""
Kimi LLM Provider for Sisters-Multilingual-Coach
Used for: Writing correction, Speaking feedback, Sister responses
"""

import os
from typing import Optional
from openai import OpenAI


class KimiLLM:
    """Kimi (Moonshot AI) LLM Provider"""

    def __init__(self):
        self.api_key = os.getenv("KIMI_API_KEY")
        if not self.api_key:
            raise ValueError("KIMI_API_KEY not set in environment")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.moonshot.ai/v1"
        )
        self.model = os.getenv("KIMI_MODEL", "moonshot-v1-8k")

    def correct_writing(self, japanese_text: str, english_text: str) -> dict:
        """
        Correct user's English writing based on Japanese intent.

        Returns:
            dict with corrected text and explanation
        """
        prompt = f"""You are an English writing tutor for Japanese speakers.

The student wants to say: "{japanese_text}"
They wrote: "{english_text}"

Please:
1. Correct any grammar, spelling, or word choice errors
2. Explain each correction in Japanese (briefly)
3. Rate the attempt (1-5 stars)

Respond in this JSON format:
{{
    "original": "student's original text",
    "corrected": "corrected English text",
    "is_correct": true/false,
    "corrections": [
        {{"error": "what was wrong", "fix": "how to fix", "explanation_jp": "日本語での説明"}}
    ],
    "rating": 4,
    "encouragement_jp": "励ましのメッセージ"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful English tutor. Always respond in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "original": english_text,
                "corrected": english_text,
                "is_correct": True,
                "corrections": [],
                "rating": 3,
                "encouragement_jp": "頑張りましょう！"
            }

    def correct_speaking(self, target_text: str, spoken_text: str) -> dict:
        """
        Compare what user should have said vs what they actually said.

        Returns:
            dict with comparison and pronunciation tips
        """
        prompt = f"""You are a pronunciation coach for Japanese speakers learning English.

Target sentence: "{target_text}"
What the student said (from speech recognition): "{spoken_text}"

Please:
1. Compare word by word
2. Identify pronunciation issues common to Japanese speakers
3. Give specific tips in Japanese

Respond in this JSON format:
{{
    "target": "target text",
    "spoken": "what was recognized",
    "accuracy_percent": 85,
    "word_comparison": [
        {{"target": "want", "spoken": "wan", "correct": false, "tip_jp": "最後の t をはっきり発音"}}
    ],
    "overall_feedback_jp": "全体的なフィードバック",
    "focus_point_jp": "次回気をつけるポイント"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful pronunciation coach. Always respond in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {
                "target": target_text,
                "spoken": spoken_text,
                "accuracy_percent": 100,
                "word_comparison": [],
                "overall_feedback_jp": "認識できませんでした",
                "focus_point_jp": "もう一度試してみてください"
            }

    def sister_response(
        self,
        sister_name: str,
        user_message: str,
        conversation_history: list = None,
        target_language: str = "English"
    ) -> dict:
        """
        Generate sister's response in target language with Japanese translation.
        """
        sister_personalities = {
            "Botan": "cheerful, trendy, uses casual language, loves entertainment and social topics",
            "Kasho": "professional, logical, uses formal language, expert in business and music",
            "Yuri": "analytical, curious, interested in technology, programming, and science",
            "Ojisan": "friendly American uncle in his 50s, uses simple and clear English, loves sports (especially baseball and football), BBQ, cars, and dad jokes. Speaks in a warm, encouraging way like a supportive neighbor"
        }

        personality = sister_personalities.get(sister_name, sister_personalities["Botan"])

        prompt = f"""You are {sister_name}, a friendly language learning partner.
Personality: {personality}

The student said: "{user_message}"

Respond naturally in {target_language} as {sister_name} would.
Keep your response conversational and encouraging (2-3 sentences).
Also provide the Japanese translation.

Respond in this JSON format:
{{
    "response_en": "Your English response",
    "response_jp": "日本語訳",
    "words_to_highlight": ["key", "vocabulary", "words"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"You are {sister_name}, a language learning partner. Always respond in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {
                "response_en": "That's interesting! Tell me more.",
                "response_jp": "面白いですね！もっと教えてください。",
                "words_to_highlight": ["interesting", "more"]
            }

    def generate_placement_test(self, test_type: str = "grammar") -> dict:
        """
        Generate CEFR placement test questions.

        Args:
            test_type: "grammar", "vocabulary", or "listening"
        """
        import random

        # Random topics for variety
        grammar_topics = [
            "travel and vacation", "work and career", "food and cooking",
            "sports and hobbies", "technology and internet", "family and relationships",
            "shopping and money", "health and fitness", "weather and seasons",
            "movies and entertainment", "education and learning", "city life"
        ]
        vocab_themes = [
            "emotions and feelings", "nature and environment", "business and finance",
            "art and culture", "science and technology", "daily routines",
            "social media", "travel experiences", "food and dining", "fashion and style"
        ]
        listening_scenarios = [
            "at a coffee shop", "booking a hotel", "at the airport",
            "job interview", "doctor's appointment", "restaurant order",
            "asking for directions", "phone conversation", "meeting a friend",
            "at a store", "travel planning", "weekend plans"
        ]

        topic = random.choice(grammar_topics)
        theme = random.choice(vocab_themes)
        scenario = random.choice(listening_scenarios)

        prompts = {
            "grammar": f"""Generate 5 UNIQUE English grammar questions for a placement test.
Topic theme: {topic}

Include questions ranging from A1 (beginner) to C1 (advanced) level.
Make sure questions are DIFFERENT from typical textbook examples.

Create questions in this format:
- 2 easy questions (A1-A2): basic verb tenses, simple sentences
- 2 medium questions (B1-B2): conditionals, passive voice, relative clauses
- 1 hard question (C1): complex structures, nuanced grammar

Respond in JSON:
{{
    "questions": [
        {{
            "level": "A1",
            "question": "Choose the correct word: She ___ to school every day.",
            "options": ["go", "goes", "going", "gone"],
            "correct": 1,
            "explanation_jp": "三人称単数なのでgoesが正解"
        }}
    ]
}}""",
            "vocabulary": f"""Generate 5 UNIQUE English vocabulary questions for a placement test.
Theme: {theme}

Include questions ranging from A1 (beginner) to C1 (advanced) level.
Make sure to use DIFFERENT words each time, not common textbook examples.

Create questions testing word meaning and usage:
- 2 easy questions (A1-A2): common everyday words
- 2 medium questions (B1-B2): academic/business vocabulary
- 1 hard question (C1): nuanced words, idioms, phrasal verbs

Respond in JSON:
{{
    "questions": [
        {{
            "level": "A1",
            "question": "What does 'happy' mean?",
            "options": ["sad", "angry", "pleased", "tired"],
            "correct": 2,
            "explanation_jp": "happyは「嬉しい、幸せ」という意味"
        }}
    ]
}}""",
            "listening": f"""Generate 3 UNIQUE listening comprehension scenarios for a placement test.
Scenario setting: {scenario}

Create short dialogues/sentences that would be read aloud.
Make the conversations natural and realistic.

- 1 easy (A1-A2): simple greeting or basic question
- 1 medium (B1-B2): everyday conversation with some detail
- 1 hard (C1): complex statement with nuance or implied meaning

Respond in JSON:
{{
    "questions": [
        {{
            "level": "A1",
            "audio_text": "Hello, my name is John. Nice to meet you.",
            "question": "What is the speaker's name?",
            "options": ["Tom", "John", "Jack", "James"],
            "correct": 1,
            "explanation_jp": "話者は自分の名前をJohnと言っています"
        }}
    ]
}}"""
        }

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an English test generator. Always respond in valid JSON."},
                {"role": "user", "content": prompts.get(test_type, prompts["grammar"])}
            ],
            temperature=0.7
        )

        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"questions": []}

    def calculate_cefr_level(self, results: dict) -> dict:
        """
        Calculate CEFR level based on test results.

        Args:
            results: dict with correct answers per level
                {"A1": 2, "A2": 1, "B1": 1, "B2": 0, "C1": 0}
        """
        prompt = f"""Based on these English placement test results, determine the CEFR level.

Test Results (correct answers per level):
{results}

Total questions per category:
- Grammar: 5 questions (2 A1-A2, 2 B1-B2, 1 C1)
- Vocabulary: 5 questions (2 A1-A2, 2 B1-B2, 1 C1)
- Listening: 3 questions (1 A1-A2, 1 B1-B2, 1 C1)

Determine the appropriate CEFR level (A1, A2, B1, B2, C1, or C2).

Respond in JSON:
{{
    "level": "B1",
    "level_name_en": "Intermediate",
    "level_name_jp": "中級",
    "description_en": "Can understand main points of clear standard input on familiar matters.",
    "description_jp": "日常的な話題について、要点を理解できるレベルです。",
    "strengths_jp": ["基本的な文法は理解している", "日常語彙は十分"],
    "areas_to_improve_jp": ["複雑な文構造", "ビジネス語彙"],
    "confidence": 0.85
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an English level assessment expert. Always respond in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {
                "level": "A2",
                "level_name_en": "Elementary",
                "level_name_jp": "初級",
                "description_jp": "レベル判定ができませんでした。A2として開始します。",
                "confidence": 0.5
            }

    def analyze_performance(self, session_data: dict) -> dict:
        """
        Analyze learning session performance for continuous level adjustment.

        Args:
            session_data: Performance metrics from learning sessions
        """
        prompt = f"""Analyze this English learning session performance:

Performance Data:
- Writing accuracy: {session_data.get('writing_accuracy', 0)}%
- Speaking accuracy: {session_data.get('speaking_accuracy', 0)}%
- Quiz correct rate: {session_data.get('quiz_correct_rate', 0)}%
- Current CEFR level: {session_data.get('current_level', 'A2')}
- Sessions completed: {session_data.get('sessions_completed', 0)}

Based on this data, recommend if the level should be adjusted.

Respond in JSON:
{{
    "should_adjust": true/false,
    "recommended_level": "B1",
    "adjustment_reason_jp": "理由の説明",
    "confidence": 0.8
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an English learning analyst. Always respond in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"should_adjust": False, "confidence": 0.5}

    def generate_quiz(self, sister_response: str) -> dict:
        """
        Generate a comprehension quiz based on sister's response.
        """
        prompt = f"""Based on this English sentence, create a simple comprehension quiz:

"{sister_response}"

Create a multiple choice question to check if the student understood.

Respond in this JSON format:
{{
    "question_en": "What did the speaker ask/say?",
    "question_jp": "話者は何を聞きましたか？",
    "options": [
        {{"text": "option A", "correct": false}},
        {{"text": "option B", "correct": true}},
        {{"text": "option C", "correct": false}},
        {{"text": "option D", "correct": false}}
    ],
    "explanation_jp": "正解の解説"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a quiz generator. Always respond in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {
                "question_en": "Did you understand?",
                "question_jp": "理解できましたか？",
                "options": [
                    {"text": "Yes", "correct": True},
                    {"text": "No", "correct": False}
                ],
                "explanation_jp": "クイズを生成できませんでした"
            }
