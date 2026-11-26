# AI Voice Studio V0.3 — Browser-Based TTS

Static PWA hosted on GitHub Pages. No Python backend, Render service, or API key.

- TTS: Kokoro-82M via kokoro-js / Transformers.js.
- Runs in the browser using WebGPU when available, otherwise WASM.
- First use downloads model/runtime files from public CDN/model hosting. Browser cache may speed up later use.
- English voices in this release: af_heart, af_bella, af_nova, am_michael. Indonesian is not supported by this initial English model.
- WAV export is generated from PCM; MP3 export uses lamejs in the browser.
- Audio history is session-only; files are not uploaded to a server.

## Deploy
GitHub Pages: Settings -> Pages -> Deploy from branch -> main -> /(root).

Open https://jerry2782.github.io/ai-voice-studio/. If an old version remains, refresh and clear site data/service worker cache.

## Notes
Use Wi-Fi on first use. The first model download can be large (tens to around 100 MB depending on runtime files). Device memory and browser support affect performance. Fully offline operation is not guaranteed until all assets are cached.

Review the licenses of Kokoro model weights, kokoro-js/Transformers.js and lamejs before commercial distribution.
