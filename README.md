# Sisters-Multilingual-Coach

Learn languages through natural conversation with the Three Sisters AI characters.

## Concept

Unlike traditional language learning apps that focus on drills and exercises, Sisters-Multilingual-Coach lets you practice through natural conversation with three unique AI personalities:

- **Botan** - Sociable, trendy, great for casual conversation practice
- **Kasho** - Professional, logical, perfect for business language
- **Yuri** - Creative, thoughtful, ideal for literature and culture topics

## Supported Languages

| Language | Status |
|----------|--------|
| English | Priority |
| 中文 (Chinese) | Priority |
| 日本語 (Japanese) | Planned |
| 한국어 (Korean) | Future |
| Español (Spanish) | Future |

## Features

- **Listen** - Sisters speak to you using natural TTS (ElevenLabs)
- **Speak** - Practice pronunciation with STT (Whisper)
- **Converse** - Natural dialogue powered by LLM
- **Feedback** - Get corrections and suggestions

## Tech Stack

- **Frontend**: Streamlit (Web UI)
- **TTS**: ElevenLabs API
- **STT**: OpenAI Whisper
- **LLM**: Kimi (Moonshot AI) / OpenAI
- **Language**: Python 3.11+

## Quick Start

```bash
# Clone repository
git clone https://github.com/koshikawa-masato/Sisters-Multilingual-Coach.git
cd Sisters-Multilingual-Coach

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
streamlit run src/app.py
```

## License

Private - All Rights Reserved

## Author

Koshikawa Masato
