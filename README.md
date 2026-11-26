# AI Voice Studio — TTS backend (prototype)

FastAPI + Piper TTS prototype. It exposes `/health`, `/voices` (planned), and `/tts`.
This backend returns MP3 by default and WAV when requested.

## Render setup

This folder is intended to be deployed as a Render Web Service with:
- Root Directory: `backend`
- Build Command: install FFmpeg, Python dependencies, then download both voice models
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

The service uses Render's ephemeral filesystem only for model files at build time.
Generated audio is returned directly to the browser; it is not stored on the server.

## Important
This is a prototype. Check the Piper engine and each voice model's license and voice quality before public/commercial use.
