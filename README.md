<div align="center">

## ⚡ GD ARENA ⚡
### *The Ultimate Voice-First AI Placement Simulator*
> **"Walk into your next Group Discussion & Tech Interview already feared and ready."**

[![GitHub Stars](https://img.shields.io/github/stars/kartikey-bhadauria/gd-arena?style=for-the-badge&color=blueviolet)](https://github.com/kartikey-bhadauria/gd-arena/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/kartikey-bhadauria/gd-arena?style=for-the-badge&color=cyan)](https://github.com/kartikey-bhadauria/gd-arena/network)
[![License](https://img.shields.io/github/license/kartikey-bhadauria/gd-arena?style=for-the-badge&color=green)](LICENSE)
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Live%20Deployment-black?style=for-the-badge&logo=vercel)](https://gd-arena-phi.vercel.app)
[![Contributors](https://img.shields.io/github/contributors/kartikey-bhadauria/gd-arena?style=for-the-badge&color=orange)](https://github.com/kartikey-bhadauria/gd-arena/graphs/contributors)

[Features](#-features) • [Who It Is For](#-who-it-is-for) • [Tools & AI Used](#️-tools--ai-used) • [How To Run It](#-how-to-run-it) • [Personas](#-meet-the-ai-cast) • [Scoring Engine](#-how-scoring-works)

</div>

---

## 🔥 What It Does (Problem Statement 2)
**GD Arena** is a zero-cost, voice-first simulation platform engineered for engineering students to master campus placement Group Discussions (GD) and technical mock interviews against multi-agent AI opponents.

Under **Problem Statement 2**, GD Arena provides:
- **Configurable Room Setup**: Custom topics and selectable panel sizing (3 or 4 AI participants).
- **AI-to-AI Discussion Loop**: Moderator opening $
ightarrow$ AI participant response to student $
ightarrow$ Inter-agent debate and moderation on timer expiration.
- **Voice & Fallback Resilience**: Real-time Web Speech STT/TTS audio synthesis and robust fallback synthesis.
- **Deterministic Placement Scoring**: Transparent post-session report analyzing speech share, keyword density, and interaction quality.

---

## 🎯 Who It Is For
- **Engineering Students & Job Seekers**: Preparing for campus placement drives (Service-based & Product-based MNCs).
- **Aspirants Lacking Peers**: Students who want realistic, high-pressure group discussion practice without needing a physical study group.
- **Technical Interview Candidates**: Anyone looking for rigorous 1-on-1 grilling on system design, scalability, and code architecture.

---

## 🛠️ Tools & AI Used
- **Backend & Server**: Python 3.11+, Flask WSGI, ThreadingHTTPServer.
- **AI & LLM Providers**: Google Gemini Flash Lite (Primary), Groq Llama 3.3 70B (Secondary), OpenRouter.
- **Speech & Audio**: `edge-tts` (Neural Text-to-Speech), Web Speech API (Speech-to-Text).
- **Frontend & Styling**: Vanilla ES6 JavaScript, Tailwind CSS, Primefold Design System, Lucide Icons.
- **Deployment & VCS**: Vercel Serverless Platform, Git & GitHub.

---

## 📋 Done / Left / Plan

| Status | Component / Milestone | Details |
| :---: | :--- | :--- |
| ✅ **DONE** | Room Setup & Panel Sizing | Custom topic input and 3/4/5 participant panel selector wired end-to-end. |
| ✅ **DONE** | AI-to-AI Discussion Loop | Multi-turn debate where AI personas refute each other and moderate on timer expiration. |
| ✅ **DONE** | Voice & TTS Resilience | Web Speech API, audio barge-in, mic denial handling, and robust fallback synthesis. |
| ✅ **DONE** | Quote-Linked Reporting | Placement report with exact transcript quotes, timestamps, word share, and turn counts. |
| ✅ **DONE** | Vercel & GitHub Deployment | Live deployment on Vercel and production GitHub repository sync. |

---

## 🏗️ Architecture & Why
```mermaid
graph TD
    A[User Voice / Mic] -->|Web Speech STT| B[Client Turn Manager]
    B -->|HTTP / JSON| C[Python ThreadingHTTPServer]
    C -->|Gemini Flash Lite / Groq| D[Multi-Agent Persona Engine]
    D -->|AI-to-AI Rebuttal Loop| C
    C -->|edge-tts Neural Audio| E[Audio Playback & VU Meter]
    C -->|Transcript & Metrics| F[Quote-Verified Scoring Engine]
    F -->|Detailed Breakdown| G[Candidate Report Dashboard]
```
**Why this architecture?** Python's standard `ThreadingHTTPServer` combined with Flask and server-sent/REST endpoints enables low-latency multi-agent orchestration without bulky WebSockets, while vanilla client-side Web Speech and Audio APIs provide seamless zero-cost speech synthesis and recognition.

---

## 🚀 What We Added
- **Multi-Agent Inter-Agent Debates**: AI models now evaluate prior AI statements for logical fallacies and cross-examine each other before turning back to the candidate.
- **Dynamic Panel Controls**: UI selectors for custom topics and panel counts (3-5 personas).
- **Quote-Linked Scoring Engine**: Replaced generic heuristics with precise quote matching from session transcripts.

---

## 🚀 Key Features

- 🎙️ **Live Voice Barge-In & Neural Audio**: Real-time voice interaction with Web Speech API and `edge-tts` neural voice synthesis.
- 🤖 **Multi-Agent AI Opponents**: Dynamic discussion rooms where AI personas argue, interrupt, refute fallacies, and synthesize points.
- 📊 **Quote-Verified Placement Scoring**: No vanity scores. Every score card cites exact timestamped quotes from the transcript and provides actionable counter-arguments.
- 📄 **Resume Intelligence**: Parses your resume (`.pdf`, `.docx`, `.txt`) to tailor interview grilling questions dynamically.
- ⚡ **Primefold Design System**: Sleek, high-performance UI built with Tailwind CSS, Lucide icons, and immersive dark/light aesthetics.

---

## 👥 Meet the AI Cast

| Persona | Role | Personality & Style |
| :--- | :--- | :--- |
| **Mr. Verma** | Moderator | Strict placement cell head; keeps order, calls out tangents, tests assertiveness. |
| **Aarav** | The Dominator | Aggressive, fast-speaker; jumps in early, cuts off weak arguments, tests rebuttal skills. |
| **Priya** | Data-Driven | Relies on benchmarks, scalability metrics, and ROI figures; destroys hand-wavy claims. |
| **Rohan** | Synthesizer | Diplomatic mediator; bridges competing viewpoints and structures chaotic consensus. |
| **Neha** | Quiet Thinker | Delivers high-impact, late-stage analytical insights that shift room momentum. |
| **Ms. Kapoor** | Tech Interviewer | 1-on-1 interviewer for FAANG-level system design and deep algorithmic grilling. |

---

## 🏗️ Architecture

```mermaid
graph TD
    A[User Voice / Mic] -->|Web Speech STT| B[Client Turn Manager]
    B -->|HTTP / JSON| C[Python ThreadingHTTPServer]
    C -->|Gemini Flash Lite / Groq| D[Multi-Agent Persona Engine]
    D -->|Turn Strategy & Refutation| C
    C -->|edge-tts Neural Audio| E[Audio Playback & VU Meter]
    C -->|Transcript & Metrics| F[Quote-Verified Scoring Engine]
    F -->|Detailed Breakdown| G[Candidate Report Dashboard]
```

---

## 🛠️ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/kartikey-bhadauria/gd-arena.git
cd gd-arena

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Add your GOOGLE_API_KEY / GEMINI_API_KEY in .env

# 4. Launch the simulator
python server.py
# Open http://localhost:8000 in your browser
```

---



## 👥 Core Contributors & Team

| Contributor | Role & Responsibilities | GitHub |
| :--- | :--- | :--- |
| **Kartikey Bhadauria** | Creator & Lead Full-Stack Architect | [@kartikey-bhadauria](https://github.com/kartikey-bhadauria) |
| **Priyanshu Pandey** | Lead UI/UX Designer (Primefold System) | *Designer* |
| **Anshuman Maurya** | Senior Frontend Developer & Interaction Engineer | *Frontend Developer* |

---

## 🤝 Contributing

Contributions, feature requests, and bug reports are welcome! 
1. Fork the repo (`https://github.com/kartikey-bhadauria/gd-arena/fork`)
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🛡️ License

Distributed under the **MIT License**. See `LICENSE` for more information.

<div align="center">
  <sub align="center">Built with ⚡ by Kartikey Bhadauria & Contributors</sub>
</div>
