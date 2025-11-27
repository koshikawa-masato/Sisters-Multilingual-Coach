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
