import io
import os
import subprocess
import wave
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field
from piper import PiperVoice, SynthesisConfig

BASE_DIR = Path(__file__).parent
VOICE_DIR = BASE_DIR / "voices"

app = FastAPI(title="AI Voice Studio TTS API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://jerry2782.github.io",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

VOICE_FILES = {
    "en-US-female": VOICE_DIR / "en_US-lessac-medium.onnx",
    "id-ID-female": VOICE_DIR / "id_ID-news_tts-medium.onnx",
}
_loaded_voices = {}

class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=3000)
    voice: Literal["en-US-female", "id-ID-female"] = "en-US-female"
    speed: float = Field(default=1.0, ge=0.75, le=1.35)
    output: Literal["mp3", "wav"] = "mp3"

@app.on_event("startup")
def load_voices():
    for key, path in VOICE_FILES.items():
        if path.exists() and Path(str(path) + ".json").exists():
            try:
                _loaded_voices[key] = PiperVoice.load(str(path))
            except Exception as exc:
                print(f"Could not load {key}: {exc}")
        else:
            print(f"Voice model missing: {path}")

@app.get("/")
def root():
    return {"name": "AI Voice Studio TTS API", "status": "ready", "docs": "/docs"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "loaded_voices": list(_loaded_voices.keys()),
        "available_voices": list(VOICE_FILES.keys()),
    }

@app.post("/tts")
def synthesize(req: TTSRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty.")
    voice = _loaded_voices.get(req.voice)
    if voice is None:
        raise HTTPException(
            status_code=503,
            detail=f"Voice {req.voice} is not loaded. Check deployment logs and model files.",
        )

    wav_buffer = io.BytesIO()
    config = SynthesisConfig(length_scale=req.speed)
    try:
        with wave.open(wav_buffer, "wb") as wav_file:
            voice.synthesize_wav(req.text.strip(), wav_file, syn_config=config)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {exc}")

    wav_bytes = wav_buffer.getvalue()
    if req.output == "wav":
        return Response(
            content=wav_bytes,
            media_type="audio/wav",
            headers={"Content-Disposition": 'attachment; filename="voice-output.wav"'},
        )

    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "wav", "-i", "pipe:0",
             "-codec:a", "libmp3lame", "-b:a", "192k", "-f", "mp3", "pipe:1"],
            input=wav_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=90,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="FFmpeg is not installed on the server.")
    except subprocess.CalledProcessError as exc:
        raise HTTPException(status_code=500, detail=exc.stderr.decode("utf-8", "ignore"))

    return Response(
        content=result.stdout,
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'attachment; filename="voice-output.mp3"'},
    )
