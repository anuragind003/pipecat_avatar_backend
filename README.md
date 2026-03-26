# Ambilio Avatar Backend

This is the **Python backend** for the Ambilio Avatar application, built with [Pipecat AI](https://github.com/pipecat-ai/pipecat). It orchestrates a real-time conversational pipeline combining speech-to-text, LLM, text-to-speech, and Simli's lip-syncing avatar technology.

## Features

- **Real-time Pipeline**: Low-latency interaction using WebRTC.
- **STT**: [Deepgram](https://www.deepgram.com/) for fast and accurate speech-to-text.
- **LLM**: [OpenAI](https://openai.com/) for intelligent conversation.
- **TTS**: Choice between [Cartesia](https://cartesia.ai/) (high quality) or XTTS (local/server).
- **Avatar**: [Simli](https://simli.com/) for high-fidelity lip-synced video avatars.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

## Getting Started

1. **Install dependencies**:

   ```bash
   cd backend
   # Using uv (fastest)
   uv sync
   # OR using pip
   python -m pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file in the `backend/` directory:

   ```ini
   TTS_SERVICE=cartesia  # 'cartesia' or 'xtts'
   OPENAI_API_KEY=your_openai_key
   DEEPGRAM_API_KEY=your_deepgram_key
   SIMLI_API_KEY=your_simli_key
   SIMLI_FACE_ID=your_face_id

   # If using Cartesia
   CARTESIA_API_KEY=your_cartesia_key
   CARTESIA_VOICE_ID=your_voice_id

   # If using XTTS
   XTTS_URL=http://localhost:8000
   XTTS_VOICE_ID=Ana Florence
   ```

3. **Run the server**:
   ```bash
   # Using uv
   uv run main.py
   # OR using python
   python main.py
   ```
   The backend will listen for connections (default port 7860 as inferred from frontend config).

## Architecture

The pipeline in `main.py` follows this flow:
`Transport Input (WebRTC) -> STT (Deepgram) -> Context Aggregator -> LLM (OpenAI) -> TTS (Cartesia/XTTS) -> Simli Video -> Transport Output`

## Notes

- **VAD**: Uses Silero VAD via Pipecat for robust voice activity detection.
- **Latency**: Ensure your server is physically close to your users for the best WebRTC experience.
- **Simli**: Requires a valid `SIMLI_FACE_ID`. You can find these in the Simli dashboard.
