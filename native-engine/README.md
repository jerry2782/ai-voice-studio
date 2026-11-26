# AI Voice Studio V0.6.0 — Native ArboTTS Engine

This folder contains a first native integration of the browser-based ArboTTS engine source.

## Open locally / publish
Serve this folder over HTTP(S), not file://. For GitHub Pages, set Pages source to branch `v0.6.0-native-arbotts` and folder `/ (root)` only if the app is moved to repository root; currently this app is nested at `/native-engine/`. If publishing the branch root, the page path is:
`https://jerry2782.github.io/ai-voice-studio/native-engine/`
This URL works only after GitHub Pages is configured to publish this branch and deployment succeeds.

## Engine assets
- `app.js`: synthesis flow and ONNX Runtime Web setup.
- `g2p.js`, `en_dict.js`: bilingual text-to-phoneme processing.
- `dsp.js`: audio processing/persona presets.
- `wav.js`: WAV encoder.
- `models/vocab.json`: phoneme vocabulary.
- ONNX model (~9 MB) and vocabulary are fetched from the official ArboTTS demo GitHub Pages origin, so first use requires internet. Model data is cached in IndexedDB by the engine.

## Current verified scope
The source integration and relative module layout have been committed. It has NOT yet been run end-to-end on GitHub Pages or tested on the user's phone. Please treat this as an integration build, not a release.

The upstream UI currently exposes five persona presets in its actual HTML/JS: Arbo, Bimo, Dimas, Danu, and Bayu. Do not advertise seven working presets until the upstream implementation actually provides them. The upstream demo README and implementation are inconsistent on this point.

Voice-cloning controls in the upstream demo perform acoustic analysis and DSP adaptation; they should not be described as a full neural voice-cloning model without further verification.

## Credits
ArboTTS source: https://github.com/ARBO-TEAM/arbotts-demo
