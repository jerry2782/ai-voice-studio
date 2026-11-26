import io
import subprocess
import wave
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field
from piper import PiperVoice

BASE_DIR = Path(__file__).resolve().parent
VOICE_MODEL = BASE_DIR / "voices" / "en_US-lessac-low.onnx"

app = FastAPI(title="AI Voice Studio API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://jerry2782.github.io",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

voice = None

class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)
    output: Literal["mp3", "wav"] = "mp3"

@app.on_event("startup")
def load_voice():
    global voice
    if not VOICE_MODEL.exists():
        print(f"Voice model not found: {VOICE_MODEL}")
        return
    try:
        voice = PiperVoice.load(str(VOICE_MODEL))
        print("Loaded single voice model: en_US-lessac-low")
    except Exception as exc:
        print(f"Voice load failed: {exc}")
        voice = None

@app.get("/")
def root():
    return {
        "app": "AI Voice Studio API",
        "version": "0.2.0",
        "status": "ready" if voice else "voice_not_loaded",
        "health": "/health",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {
        "status": "ok" if voice else "degraded",
        "engine": "Piper TTS",
        "voice": "en_US-lessac-low",
        "voice_loaded": voice is not None,
    }

@app.post("/tts")
def synthesize(req: TTSRequest):
    if voice is None:
        raise HTTPException(
            status_code=503,
            detail="Voice model is not loaded. Check Render build logs.",
        )

    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    wav_buffer = io.BytesIO()
    try:
        with wave.open(wav_buffer, "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {exc}")

    wav_bytes = wav_buffer.getvalue()
    if req.output == "wav":
        return Response(
            content=wav_bytes,
            media_type="audio/wav",
            headers={"Content-Disposition": 'attachment; filename="ai-voice-output.wav"'},
        )

    try:
        converted = subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error",
                "-i", "pipe:0", "-vn", "-codec:a", "libmp3lame",
                "-b:a", "128k", "-f", "mp3", "pipe:1",
            ],
            input=wav_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=45,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="FFmpeg is missing on the server.")
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="MP3 conversion timed out.")
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.decode("utf-8", "ignore")[-800:]
        raise HTTPException(status_code=500, detail=f"MP3 conversion failed: {detail}")

    return Response(
        content=converted.stdout,
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'attachment; filename="ai-voice-output.mp3"'},
    )
