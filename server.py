import os
import sys
import json
import io
import time
import uuid
import asyncio
import urllib.request
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

from server.personas import PERSONAS
from server.turn_engine import TurnEngine
from server.report_engine import score_session_stats, generate_report_json
from server.resume_parser import parse_resume_text, match_jd_skills

PORT = 8000
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

# Load environment variables
def load_env():
    env_vars = {}
    paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
        r"C:\Users\Kartikey\AppData\Local\hermes\.env"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            k, v = line.split('=', 1)
                            env_vars[k.strip()] = v.strip().strip('"').strip("'")
            except Exception as e:
                print(f"Error loading {p}: {e}")
    return env_vars

ENV = load_env()
GOOGLE_KEY = ENV.get('GEMINI_API_KEY') or ENV.get('GOOGLE_API_KEY', '')
GROQ_KEY = ENV.get('GROQ_API_KEY', '')
OPENROUTER_KEY = ENV.get('OPENROUTER_API_KEY', '')

# In-memory session store
SESSIONS = {}

class GDArenaServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            pass

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Health endpoint
        if path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            health_data = {
                "ok": True,
                "gemini": bool(GOOGLE_KEY),
                "groq": bool(GROQ_KEY),
                "openrouter": bool(OPENROUTER_KEY),
                "edge_tts": HAS_EDGE_TTS,
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(health_data).encode('utf-8'))
            return

        # Session inspection
        if path.startswith('/api/session/'):
            s_id = path.split('/')[-1]
            session = SESSIONS.get(s_id)
            if session:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(session).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Session not found"}).encode('utf-8'))
            return

        # Root route
        if path == '/' or path == '':
            self.path = '/index.html'

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. Start Session
        if path == '/api/session/start':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            mode = payload.get('mode', 'gd')
            topic = payload.get('topic', 'Will Generative AI Replace Entry-Level Software Engineers?')
            panel_size = int(payload.get('panel_size', 4))
            s_id = str(uuid.uuid4())[:8]

            turn_engine = TurnEngine()

            if mode == 'interview':
                opening_text = f"Good morning. I am Ms. Kapoor. We are evaluating candidates for our technical placement drive. Let us begin with your background and your approach to '{topic}'. Tell me about your practical experience."
                mod_key = "interviewer"
            else:
                opening_text = f"Good morning candidates. I am Mr. Verma, your moderator. All other participants are AI. Today's GD topic is: '{topic}'. You have 8 minutes. The floor is open."
                mod_key = "moderator"

            session_data = {
                "id": s_id,
                "mode": mode,
                "topic": topic,
                "panel_size": panel_size,
                "start_time": time.time(),
                "turn_engine": turn_engine,
                "transcript": [
                    {
                        "id": 1,
                        "speaker": mod_key,
                        "name": PERSONAS[mod_key]["name"],
                        "role": PERSONAS[mod_key]["role"],
                        "timestamp": "00:05",
                        "text": opening_text
                    }
                ],
                "interruptions": 0
            }
            SESSIONS[s_id] = session_data

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "session_id": s_id,
                "opening": opening_text,
                "speaker": mod_key,
                "moderator_voice": PERSONAS[mod_key]["voice"],
                "topic": topic
            }).encode('utf-8'))
            return

        # 2. Chat / Dialogue Turn Orchestration
        if path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            s_id = payload.get('session_id')
            student_text = payload.get('text', '').strip()
            interrupted = payload.get('interrupted', False)

            session = SESSIONS.get(s_id)
            if not session:
                # Create ad-hoc session
                session = {
                    "id": s_id or "temp",
                    "mode": payload.get('mode', 'gd'),
                    "topic": payload.get('topic', 'Technology & Campus Placements'),
                    "turn_engine": TurnEngine(),
                    "transcript": [],
                    "interruptions": 0
                }
                SESSIONS[session["id"]] = session

            turn_engine = session["turn_engine"]

            # Record student turn
            if student_text:
                turn_engine.note_student_spoke(interrupted=interrupted)
                if interrupted:
                    session["interruptions"] += 1

                session["transcript"].append({
                    "id": len(session["transcript"]) + 1,
                    "speaker": "student",
                    "name": "You (Candidate)",
                    "role": "Candidate",
                    "timestamp": payload.get('timestamp', '01:30'),
                    "text": student_text
                })

            # Determine next AI speaker
            next_spk = turn_engine.next_speaker(mode=session["mode"])
            persona = PERSONAS.get(next_spk, PERSONAS["aarav"])
            turn_engine.note_ai_spoke(next_spk)

            # Generate AI dialogue turn
            ai_text = self.generate_llm_turn(persona, session["topic"], session["mode"], student_text, session["transcript"])

            session["transcript"].append({
                "id": len(session["transcript"]) + 1,
                "speaker": next_spk,
                "name": persona["name"],
                "role": persona["role"],
                "timestamp": payload.get('timestamp', '01:45'),
                "text": ai_text
            })

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "speaker": next_spk,
                "persona": persona["name"],
                "role": persona["role"],
                "text": ai_text,
                "voice": persona["voice"],
                "rate": persona["rate"],
                "pitch": persona["pitch"],
                "color": persona["color"]
            }).encode('utf-8'))
            return

        # 3. Dual Engine TTS Endpoint (Edge-TTS & Groq Neural TTS)
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

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        audio_bytes = loop.run_until_complete(run_tts())
                    finally:
                        loop.close()

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
            return

        # 4. Generate Placement Report
        if path == '/api/report':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            s_id = payload.get('session_id')
            session = SESSIONS.get(s_id, {})
            transcript = session.get('transcript', payload.get('transcript', []))
            topic = session.get('topic', 'Campus Placement Simulation')
            interruptions = session.get('interruptions', 0)

            stats = score_session_stats(transcript, interruptions)
            report_data = generate_report_json(transcript, topic, stats)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(report_data).encode('utf-8'))
            return

        # 5. Resume Parser & JD Match
        if path == '/api/parse-resume':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
            except Exception:
                payload = {}

            resume_text = payload.get('text', '')
            jd_text = payload.get('jd_text', '')

            parsed = parse_resume_text(resume_text)
            if jd_text:
                parsed["jd_match"] = match_jd_skills(parsed["skills"], jd_text)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(parsed).encode('utf-8'))
            return

        super().do_POST()

    def generate_llm_turn(self, persona, topic, mode, student_text, transcript):
        system_instruction = persona["system_prompt"].format(topic=topic)
        recent_context = "\n".join([f"{t['name']}: {t['text']}" for t in transcript[-4:]])

        prompt = f"""{system_instruction}

Recent Discussion Context:
{recent_context}

Last statement by Candidate: "{student_text}"

Respond as {persona['name']} in 1-2 spoken sentences (under 35 words). No markdown, no quotes, no asterisks:"""

        # 1. Primary: Google Gemini Flash Lite
        if GOOGLE_KEY:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={GOOGLE_KEY}"
                req = urllib.request.Request(
                    url,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"maxOutputTokens": 75, "temperature": 0.7}
                    }).encode('utf-8')
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    res_json = json.loads(resp.read().decode('utf-8'))
                    text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
                    return text.replace('*', '').replace('"', '').replace('\n', ' ')
            except Exception as e:
                print(f"Gemini API fallback error: {e}")

        # 2. Fallback: OpenRouter
        if OPENROUTER_KEY:
            try:
                req = urllib.request.Request(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"},
                    data=json.dumps({
                        "model": "meta-llama/llama-3.3-70b-instruct",
                        "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}],
                        "max_tokens": 70
                    }).encode('utf-8')
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    res_json = json.loads(resp.read().decode('utf-8'))
                    return res_json['choices'][0]['message']['content'].strip().replace('*', '')
            except Exception as e:
                print(f"OpenRouter API fallback error: {e}")

        # Default fallback
        fallbacks = {
            "aarav": "I strongly challenge that point. In production systems, unverified assumptions cause immediate outages.",
            "priya": "According to industry benchmarks, over seventy percent of companies measure latency trade-offs before deploying.",
            "rohan": "That is a valid point. Let us balance that with developer maintainability and team velocity.",
            "neha": "Have we considered the fundamental constraint here, or are we just optimizing the surface metrics?",
            "moderator": "Thank you. Let us hear from candidates who have not yet spoken.",
            "interviewer": "Tell me how you handled database locks and cache stampedes under heavy traffic in your project."
        }
        return fallbacks.get(persona["name"].lower(), "Let us analyze the trade-offs before drawing a conclusion.")

def run_server():
    server_address = ('', PORT)
    httpd = ThreadingHTTPServer(server_address, GDArenaServerHandler)
    print(f"=====================================================")
    print(f" GD Arena Production Server Active: http://localhost:{PORT}")
    print(f" Google Gemini: {'READY' if GOOGLE_KEY else 'MISSING'}")
    print(f" Edge Neural TTS: {'ACTIVE' if HAS_EDGE_TTS else 'DISABLED'}")
    print(f" Design System: Primefold Light/Clean Theme")
    print(f"=====================================================")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
