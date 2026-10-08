import os
import json

BASE_DIR = r"C:\Users\Kartikey\gd-arena"

# 1. data/topics.json
topics_data = {
  "abstract": [
    "Is failure a better teacher than success?",
    "Can money buy happiness?",
    "Is ambition overrated?",
    "Does social media connect or isolate us?"
  ],
  "controversial": [
    "Should campus placements be abolished?",
    "Is AI a threat to white-collar jobs?",
    "Should coding be mandatory in schools?",
    "Is work-from-home killing company culture?"
  ],
  "case_based": [
    "A startup has 6 months of runway. Should they pivot or double down?",
    "A college wants to ban smartphones. How would you implement it?",
    "A product has high engagement but no revenue. What do you do?"
  ],
  "current_affairs": [
    "Should AI replace teachers in schools?",
    "Is the 4-day workweek viable in India?",
    "Should internships be paid?",
    "Is remote work here to stay?"
  ],
  "campus_placement": [
    "Should companies hire based on CGPA?",
    "Is a Tier-2 college degree a disadvantage?",
    "Should students take gap years to upskill?",
    "Is a service company the right first job?"
  ]
}

with open(os.path.join(BASE_DIR, "data", "topics.json"), "w", encoding="utf-8") as f:
    json.dump(topics_data, f, indent=2)

# 2. data/rubric.json
rubric_data = {
  "dimensions": {
    "opening": { "weight": 1.5, "min_pass": 5, "label": "Opening Statement & Initiation" },
    "idea_quality": { "weight": 2.0, "min_pass": 5, "label": "Idea Quality & Logical Reasoning" },
    "building_on_others": { "weight": 1.5, "min_pass": 4, "label": "Building on Others & Synthesis" },
    "listening": { "weight": 1.5, "min_pass": 5, "label": "Active Listening & Composure" },
    "handling_interruptions": { "weight": 1.0, "min_pass": 4, "label": "Handling Interruptions & Rebuttals" },
    "closing": { "weight": 1.5, "min_pass": 5, "label": "Closing Synthesis & Conclusion" }
  },
  "tiers": {
    "weak": { "range": [0, 4], "label": "Weak", "meaning": "You'd get cut in Round 1" },
    "average": { "range": [4, 6], "label": "Average", "meaning": "You'd survive, not stand out" },
    "strong": { "range": [6, 8], "label": "Strong", "meaning": "You'd get shortlisted" },
    "elite": { "range": [8, 10], "label": "Elite", "meaning": "You'd lead the room" }
  },
  "red_flags": [
    "Zero speaking time in first 90 seconds",
    "Contradicting self without acknowledgment",
    "Interrupting more than 4 times",
    "No references to other participants",
    "Off-topic for more than 30 seconds without recovery"
  ]
}

with open(os.path.join(BASE_DIR, "data", "rubric.json"), "w", encoding="utf-8") as f:
    json.dump(rubric_data, f, indent=2)

# 3. data/config.json
config_data = {
  "durations": [5, 8, 15],
  "phases": ["Opening", "Discussion", "Closing"],
  "reactionDelay": 1350,
  "silenceThreshold": 900,
  "maxAITurnsInARow": 2,
  "defaultPanelSize": 4,
  "sampleScenarios": {
    "interview": [
      "Technical Core & Scalability Architecture",
      "Behavioral Conflict & Leadership Under Pressure",
      "System Design & Database Failure Modes"
    ],
    "gd": [
      "Should AI Replace Software Engineers in Campus Hiring?",
      "Monolith vs Microservices for Seed-Stage Startups",
      "Should Engineering Colleges Eliminate CGPA Filters?"
    ]
  }
}

with open(os.path.join(BASE_DIR, "data", "config.json"), "w", encoding="utf-8") as f:
    json.dump(config_data, f, indent=2)

# 4. requirements.txt
reqs = """edge-tts>=7.2.7
requests>=2.31.0
aiohttp>=3.9.0
python-dotenv>=1.0.0
"""
with open(os.path.join(BASE_DIR, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write(reqs)

# 5. Procfile
with open(os.path.join(BASE_DIR, "Procfile"), "w", encoding="utf-8") as f:
    f.write("web: python server.py\n")

# 6. .env.example & .env
env_example = """GOOGLE_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
PORT=8000
ENV=development
"""
with open(os.path.join(BASE_DIR, ".env.example"), "w", encoding="utf-8") as f:
    f.write(env_example)

env_real = """GOOGLE_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
PORT=8000
ENV=development
"""
with open(os.path.join(BASE_DIR, ".env"), "w", encoding="utf-8") as f:
    f.write(env_real)

# 7. .gitignore
gitignore_content = """.env
*.env
__pycache__/
*.pyc
*.wav
*.mp3
node_modules/
.DS_Store
*.log
"""
with open(os.path.join(BASE_DIR, ".gitignore"), "w", encoding="utf-8") as f:
    f.write(gitignore_content)

# 8. README.md & PROJECT_CONTEXT.md
readme = """# GD Arena — Voice-First AI Interview & Group Discussion Simulator

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
"""
with open(os.path.join(BASE_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)

with open(os.path.join(BASE_DIR, "PROJECT_CONTEXT.md"), "w", encoding="utf-8") as f:
    f.write(readme)

# 9. server/__init__.py
with open(os.path.join(BASE_DIR, "server", "__init__.py"), "w", encoding="utf-8") as f:
    f.write('"""GD Arena Backend Package"""\n')

print("Phase 1 files created successfully!")
