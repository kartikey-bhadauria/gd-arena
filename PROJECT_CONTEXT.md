# GD Arena — Voice-First AI Interview & Group Discussion Simulator

> **"Walk into your next GD already ready."**  
> Real GD pressure. Zero real-world risk. Speak. Interrupt. Build. Get judged honestly.

## What it does
GD Arena is a zero-cost, voice-first simulation platform where engineering students practice high-stakes campus placement Group Discussions (against 3–5 realistic AI candidate personas + 1 moderator) and 1-on-1 technical mock interviews with instant voice barge-in and quote-verified placement scoring.

## Features
- **Realistic AI Personas**: Mr. Verma (Moderator), Aarav (The Dominator), Priya (Data-Driven), Rohan (Synthesizer), Neha (Quiet Thinker), and Ms. Kapoor (Senior Interviewer).
- **Middle Command Opponent Reasoning**: AI candidates argue with internal strategy, refuting logical fallacies and citing benchmark tradeoffs.
- **Strict Placement Scoring**: No auto-pass. Every score card quotes actual transcript lines with timestamps and drills.
- **Primefold Design System**: Light, clean, typography-led B2B interface.

## Tech Stack
- **Frontend**: HTML5 + Vanilla JS + Tailwind CSS CDN + Lucide Icons + Web Speech/Audio API.
- **Backend**: Python 3.11+ ThreadingHTTPServer + edge-tts neural voice synthesis + Google Gemini Free Flash Lite.

## How to Run
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start server
python server.py
# Open http://localhost:8000 in your browser
```
