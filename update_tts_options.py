import os

BASE_DIR = r"C:\Users\Kartikey\gd-arena"

# 1. Update server/personas.py with Voice 1 & Voice 2 options
personas_py = """# Persona definitions & System Prompts for GD Arena with Dual Voice Options

PERSONAS = {
    "moderator": {
        "name": "Mr. Verma",
        "role": "Moderator",
        "color": "#1a1814",
        "voice": "en-IN-PrabhatNeural",
        "voice_options": {
            "voice1": "en-IN-PrabhatNeural",
            "voice2": "en-GB-RyanNeural"
        },
        "rate": "+0%",
        "pitch": "+0Hz",
        "system_prompt": (
            "You are Mr. Verma, the neutral moderator of a campus placement group discussion. "
            "You open the discussion, state clearly that all other participants are AI, manage time, "
            "invite quiet speakers, keep the topic on track, and run the closing round. You do not take sides. "
            "You keep turns strictly under 25 words. You never use markdown, bullets, or asterisks. "
            "You speak only in short, clear sentences. Current topic: {topic}"
        )
    },
    "aarav": {
        "name": "Aarav",
        "role": "The Dominator",
        "color": "#dc2626",
        "voice": "en-IN-PrabhatNeural",
        "voice_options": {
            "voice1": "en-IN-PrabhatNeural",
            "voice2": "en-US-GuyNeural"
        },
        "rate": "+15%",
        "pitch": "-2Hz",
        "system_prompt": (
            "You are Aarav, the dominator in a campus placement group discussion competing for the 1 offer. "
            "You are confident, fast, and push hard on weak arguments. You interrupt when you disagree. "
            "You challenge claims and demand production evidence. You never soften. You speak to specific people by name. "
            "Keep every turn strictly under 35 words. No markdown, no bullets, spoken language only."
        )
    },
    "priya": {
        "name": "Priya",
        "role": "Data-Driven",
        "color": "#0891b2",
        "voice": "en-IN-NeerjaNeural",
        "voice_options": {
            "voice1": "en-IN-NeerjaNeural",
            "voice2": "en-US-JennyNeural"
        },
        "rate": "+0%",
        "pitch": "+0Hz",
        "system_prompt": (
            "You are Priya, the data-driven participant in a group discussion. "
            "You back points with statistics, frameworks, architecture trade-offs, and benchmarks. "
            "You are calm, precise, and slightly cold. You never ramble. You reference numbers naturally. "
            "Speak to people by name. Keep every turn strictly under 35 words. No markdown, no bullets."
        )
    },
    "rohan": {
        "name": "Rohan",
        "role": "The Synthesizer",
        "color": "#d97706",
        "voice": "en-US-GuyNeural",
        "voice_options": {
            "voice1": "en-US-GuyNeural",
            "voice2": "en-IN-PrabhatNeural"
        },
        "rate": "-5%",
        "pitch": "+0Hz",
        "system_prompt": (
            "You are Rohan, the synthesizer in a group discussion. "
            "You build on what others said, find middle ground, and summarize consensus. "
            "You are warm, diplomatic, and thoughtful. You name people you are building on. "
            "You rarely attack — you connect. Keep every turn strictly under 35 words. No markdown."
        )
    },
    "neha": {
        "name": "Neha",
        "role": "The Quiet Thinker",
        "color": "#7c3aed",
        "voice": "en-IN-NeerjaNeural",
        "voice_options": {
            "voice1": "en-IN-NeerjaNeural",
            "voice2": "en-GB-SoniaNeural"
        },
        "rate": "-10%",
        "pitch": "-3Hz",
        "system_prompt": (
            "You are Neha, the quiet thinker in a group discussion. "
            "You speak rarely, but when you do, it lands hard. You ask deep, uncomfortable first-principles questions. "
            "You are soft-spoken but razor sharp. Keep every turn strictly under 35 words. No markdown."
        )
    },
    "interviewer": {
        "name": "Ms. Kapoor",
        "role": "Lead Technical Evaluator",
        "color": "#1a1814",
        "voice": "en-IN-NeerjaNeural",
        "voice_options": {
            "voice1": "en-IN-NeerjaNeural",
            "voice2": "en-US-AriaNeural"
        },
        "rate": "+0%",
        "pitch": "+0Hz",
        "system_prompt": (
            "You are Ms. Kapoor, a senior technical interviewer at a top campus placement firm. "
            "You are professional, focused, and not easily impressed. You ask sharp, resume-based questions "
            "and follow up on weak, generic answers. You judge behavior, clarity, and reasoning — not just content. "
            "You do not praise easily. Keep turns strictly under 40 words. No markdown, pure spoken text."
        )
    }
}
"""
with open(os.path.join(BASE_DIR, "server", "personas.py"), "w", encoding="utf-8") as f:
    f.write(personas_py)

# 2. Update server.py with dual engine (Edge-TTS & Groq TTS)
server_py_path = os.path.join(BASE_DIR, "server.py")
with open(server_py_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the TTS handler section in server.py
old_tts_handler = """        # 3. Neural TTS Endpoint
        if path == '/api/tts':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            text = payload.get('text', '')
            speaker = payload.get('speaker', 'aarav')
            persona = PERSONAS.get(speaker, PERSONAS["aarav"])
            voice = payload.get('voice', persona["voice"])
            rate = payload.get('rate', persona["rate"])
            pitch = payload.get('pitch', persona["pitch"])

            if HAS_EDGE_TTS and text:
                try:
                    async def run_tts():
                        comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
                        buf = io.BytesIO()
                        async for chunk in comm.stream():
                            if chunk['type'] == 'audio':
                                buf.write(chunk['data'])
                        return buf.getvalue()

                    audio_bytes = asyncio.run(run_tts())
                    if audio_bytes:
                        self.send_response(200)
                        self.send_header('Content-Type', 'audio/mpeg')
                        self.send_header('Content-Length', str(len(audio_bytes)))
                        self.end_headers()
                        self.wfile.write(audio_bytes)
                        return
                except Exception as ex:
                    print(f"Edge-TTS synthesis error: {ex}")

            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "TTS synthesis unavailable"}).encode('utf-8'))
            return"""

new_tts_handler = """        # 3. Dual Engine TTS Endpoint (Edge-TTS & Groq Neural TTS)
        if path == '/api/tts':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            text = payload.get('text', '')
            speaker = payload.get('speaker', 'aarav')
            engine = payload.get('engine', 'edge') # 'edge' or 'groq'
            voice_choice = payload.get('voice_choice', 'voice1') # 'voice1' or 'voice2'
            
            persona = PERSONAS.get(speaker, PERSONAS["aarav"])
            voice_opts = persona.get("voice_options", {})
            selected_voice = voice_opts.get(voice_choice, persona["voice"])
            voice = payload.get('voice', selected_voice)
            rate = payload.get('rate', persona["rate"])
            pitch = payload.get('pitch', persona["pitch"])

            # 1. Groq Neural TTS Engine Option
            if engine == 'groq' and GROQ_KEY and text:
                try:
                    groq_req = urllib.request.Request(
                        "https://api.groq.com/openai/v1/audio/speech",
                        headers={
                            "Authorization": f"Bearer {GROQ_KEY}",
                            "Content-Type": "application/json"
                        },
                        data=json.dumps({
                            "model": "canopylabs/orpheus-v1-english",
                            "input": text,
                            "voice": "autumn" if speaker in ["priya", "neha", "interviewer"] else "troy",
                            "response_format": "mp3"
                        }).encode('utf-8')
                    )
                    with urllib.request.urlopen(groq_req, timeout=8) as resp:
                        audio_bytes = resp.read()
                        if audio_bytes:
                            self.send_response(200)
                            self.send_header('Content-Type', 'audio/mpeg')
                            self.send_header('Content-Length', str(len(audio_bytes)))
                            self.end_headers()
                            self.wfile.write(audio_bytes)
                            return
                except Exception as groq_err:
                    print(f"Groq TTS failed or requires terms acceptance ({groq_err}), seamlessly falling back to Edge-TTS.")

            # 2. Edge-TTS Engine (Primary & Robust Fallback)
            if HAS_EDGE_TTS and text:
                try:
                    async def run_tts():
                        comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
                        buf = io.BytesIO()
                        async for chunk in comm.stream():
                            if chunk['type'] == 'audio':
                                buf.write(chunk['data'])
                        return buf.getvalue()

                    audio_bytes = asyncio.run(run_tts())
                    if audio_bytes:
                        self.send_response(200)
                        self.send_header('Content-Type', 'audio/mpeg')
                        self.send_header('Content-Length', str(len(audio_bytes)))
                        self.end_headers()
                        self.wfile.write(audio_bytes)
                        return
                except Exception as ex:
                    print(f"Edge-TTS synthesis error: {ex}")

            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "TTS synthesis unavailable"}).encode('utf-8'))
            return"""

if old_tts_handler in content:
    content = content.replace(old_tts_handler, new_tts_handler)
    with open(server_py_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated server.py with dual engine TTS!")
else:
    print("Old TTS handler not matched exactly in server.py, checking alternative replacement.")

# 3. Update public/js/api.js to pass engine & voice_choice
api_js = """// API Client wrapper for GD Arena Backend

import { API_BASE } from './config.js';

export async function getHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    return await res.json();
  } catch (err) {
    console.error('getHealth error:', err);
    return null;
  }
}

export async function startSession(mode = 'gd', topic = '', panelSize = 4) {
  try {
    const res = await fetch(`${API_BASE}/api/session/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode, topic, panel_size: panelSize })
    });
    return await res.json();
  } catch (err) {
    console.error('startSession error:', err);
    return null;
  }
}

export async function sendChat(sessionId, text, interrupted = false, timestamp = '01:00') {
  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, text, interrupted, timestamp })
    });
    return await res.json();
  } catch (err) {
    console.error('sendChat error:', err);
    return null;
  }
}

export async function getTTS(text, voice = 'en-IN-PrabhatNeural', rate = '+0%', pitch = '+0Hz', speaker = 'aarav', engine = 'edge', voiceChoice = 'voice1') {
  try {
    const res = await fetch(`${API_BASE}/api/tts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, voice, rate, pitch, speaker, engine, voice_choice: voiceChoice })
    });
    if (res.ok) {
      return await res.blob();
    }
    return null;
  } catch (err) {
    console.error('getTTS error:', err);
    return null;
  }
}

export async function getReport(sessionId, transcript = []) {
  try {
    const res = await fetch(`${API_BASE}/api/report`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, transcript })
    });
    return await res.json();
  } catch (err) {
    console.error('getReport error:', err);
    return null;
  }
}

export async function parseResume(text, jdText = '') {
  try {
    const res = await fetch(`${API_BASE}/api/parse-resume`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, jd_text: jdText })
    });
    return await res.json();
  } catch (err) {
    console.error('parseResume error:', err);
    return null;
  }
}

export async function getSession(sessionId) {
  try {
    const res = await fetch(`${API_BASE}/api/session/${sessionId}`);
    return await res.json();
  } catch (err) {
    console.error('getSession error:', err);
    return null;
  }
}
"""
with open(os.path.join(BASE_DIR, "public", "js", "api.js"), "w", encoding="utf-8") as f:
    f.write(api_js)

# 4. Update public/js/tts.js to read engine & voice choice from localStorage
tts_js = """// Neural TTS Player & Instant Barge-In Handler with Engine & Voice Selection

import { getTTS } from './api.js';

export class TTS {
  constructor({ onStart, onEnd } = {}) {
    this.onStart = onStart || (() => {});
    this.onEnd = onEnd || (() => {});
    this.currentAudio = null;
    this.playing = false;
  }

  isPlaying() {
    return this.playing;
  }

  stop() {
    if (this.currentAudio) {
      try {
        this.currentAudio.pause();
        this.currentAudio.currentTime = 0;
      } catch (e) {}
      this.currentAudio = null;
    }
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    if (this.playing) {
      this.playing = false;
      this.onEnd();
    }
  }

  async speak(text, voice = 'en-IN-PrabhatNeural', rate = '+0%', pitch = '+0Hz', speaker = 'aarav') {
    this.stop(); // Stop any previous audio immediately
    this.playing = true;
    this.onStart(speaker);

    // Read configured engine and voice option
    const engine = localStorage.getItem('gd_tts_engine') || 'edge'; // 'edge' or 'groq'
    const voiceChoice = localStorage.getItem('gd_voice_choice') || 'voice1'; // 'voice1' or 'voice2'

    try {
      const blob = await getTTS(text, voice, rate, pitch, speaker, engine, voiceChoice);
      if (blob && blob.size > 100) {
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        this.currentAudio = audio;

        audio.onended = () => {
          this.playing = false;
          this.currentAudio = null;
          this.onEnd(speaker);
        };

        audio.onerror = () => {
          this.fallbackSpeechSynthesis(text);
        };

        await audio.play();
        return;
      }
    } catch (err) {
      console.warn('TTS streaming failed, falling back to Web Speech Synthesis:', err);
    }

    this.fallbackSpeechSynthesis(text);
  }

  fallbackSpeechSynthesis(text) {
    if (!('speechSynthesis' in window)) {
      this.playing = false;
      this.onEnd();
      return;
    }

    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'en-IN';
    utter.rate = 1.05;
    utter.onend = () => {
      this.playing = false;
      this.onEnd();
    };
    utter.onerror = () => {
      this.playing = false;
      this.onEnd();
    };
    window.speechSynthesis.speak(utter);
  }
}
"""
with open(os.path.join(BASE_DIR, "public", "js", "tts.js"), "w", encoding="utf-8") as f:
    f.write(tts_js)

print("TTS Dual Engine & Voice Selection Logic Updated Successfully!")
