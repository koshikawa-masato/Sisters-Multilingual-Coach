# Sisters-Multilingual-Coach

AI-powered language learning through natural conversation with unique character personalities.

## Demo

**Live Demo**: https://sisters-coach.ngrok.dev/?native=en&target=ja&level=A1&char=Botan

## Concept

Unlike traditional language learning apps that focus on drills and exercises, Sisters-Multilingual-Coach lets you practice through natural conversation with four unique AI personalities.

### Characters

| Character | Personality | Best For |
|-----------|-------------|----------|
| **Botan** | Cheerful, trendy, casual | Daily conversation, entertainment, social topics |
| **Kasho** | Professional, logical, formal | Business English, presentations, meetings |
| **Yuri** | Analytical, curious, tech-savvy | Technology, programming, science topics |
| **Ojisan** | Friendly American uncle, warm | Simple English, sports, everyday life |

## Features

### CEFR Level Assessment
- Initial placement test (Grammar, Vocabulary, Listening)
- Automatic level detection (A1-C2)
- Continuous performance tracking
- Dynamic level adjustment recommendations

### 9-Step Learning Flow

| Step | Name | Description |
|------|------|-------------|
| 1 | Japanese Input | Write what you want to say in Japanese |
| 2 | Writing | Write it in English |
| 3 | Correction | AI corrects your English |
| 4 | Speaking | Read aloud with example audio |
| 5 | Pronunciation Check | Get pronunciation feedback via STT |
| 6 | Listening | Hear all 4 characters respond |
| 7 | Reading | Bilingual display (English + Japanese) |
| 8 | Quiz | Comprehension check |
| 9 | Feedback | Session summary and next steps |

### Core Capabilities

- **Listen** - Characters speak using natural TTS (ElevenLabs)
- **Speak** - Real microphone recording with speech recognition (OpenAI Whisper)
- **Converse** - Natural dialogue powered by LLM
- **Feedback** - Detailed corrections and improvement suggestions

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| TTS | ElevenLabs API |
| STT | OpenAI Whisper |
| LLM | Kimi (Moonshot AI) |
| Language | Python 3.11+ |

## Quick Start

```bash
# Clone repository
git clone https://github.com/koshikawa-masato/Sisters-Multilingual-Coach.git
cd Sisters-Multilingual-Coach

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys:
# - ELEVENLABS_API_KEY
# - OPENAI_API_KEY
# - KIMI_API_KEY

# Run
streamlit run src/app.py
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ELEVENLABS_API_KEY` | ElevenLabs API key for TTS |
| `OPENAI_API_KEY` | OpenAI API key for Whisper STT |
| `KIMI_API_KEY` | Moonshot AI API key for LLM |
| `ELEVENLABS_VOICE_ID_BOTAN` | Voice ID for Botan character |
| `ELEVENLABS_VOICE_ID_KASHO` | Voice ID for Kasho character |
| `ELEVENLABS_VOICE_ID_YURI` | Voice ID for Yuri character |
| `ELEVENLABS_VOICE_ID_USER` | Voice ID for Ojisan/example |

## Supported Languages

| Language | Status |
|----------|--------|
| English | Active |
| 中文 (Chinese) | Planned |
| 日本語 (Japanese) | Planned |
| 한국어 (Korean) | Future |
| Español (Spanish) | Future |

## Background

This project was born from the frustration of failing an English interview. Instead of giving up, I decided to build my own AI-powered tool to improve my English speaking and listening skills.

**Goal**: Turn interview failure into product success.

## License

MIT License

## Author

**Koshikawa Masato**

- GitHub: [@koshikawa-masato](https://github.com/koshikawa-masato)
