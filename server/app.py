import os
import sys
import json
import io
import time
import uuid
import asyncio
import urllib.request
import urllib.parse
import ssl
import re
import tempfile
from flask import Flask, request, jsonify, Response, send_from_directory

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configure resilient SSL context for dev/proxy environments
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception:
    pass

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

from server.personas import PERSONAS
from server.turn_engine import TurnEngine
from server.report_engine import score_session_stats, generate_report_json
from server.resume_parser import parse_resume_text, match_jd_skills

DIRECTORY = os.path.join(PROJECT_ROOT, "server", "public")
if not os.path.exists(DIRECTORY):
    DIRECTORY = os.path.join(PROJECT_ROOT, "public")
if not os.path.exists(DIRECTORY):
    for alt in [os.path.join(os.getcwd(), "server", "public"), os.path.join(os.getcwd(), "public"), "/var/task/server/public", "/var/task/public", os.path.join(os.path.dirname(__file__), "..", "server", "public")]:
        if os.path.exists(alt):
            DIRECTORY = alt
            break

# Load environment variables
def load_env():
    env_vars = dict(os.environ)
    paths = [
        os.path.join(PROJECT_ROOT, ".env"),
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
                            k_clean = k.strip()
                            if k_clean not in env_vars or not env_vars[k_clean]:
                                env_vars[k_clean] = v.strip().strip('"').strip("'")
            except Exception as e:
                print(f"Error loading {p}: {e}")
    return env_vars

ENV = load_env()
PORT = int(ENV.get('PORT', 8000))
GOOGLE_KEY = ENV.get('GEMINI_API_KEY') or ENV.get('GOOGLE_API_KEY', '')
GROQ_KEY = ENV.get('GROQ_API_KEY', '')
OPENROUTER_KEY = ENV.get('OPENROUTER_API_KEY', '')


# In-memory session store + /tmp persistence for serverless reliability
SESSIONS = {}

def save_session(s_id, data):
    SESSIONS[s_id] = data
    try:
        tmp_path = os.path.join(tempfile.gettempdir(), f"gd_session_{s_id}.json")
        save_data = dict(data)
        if "turn_engine" in save_data:
            te = save_data["turn_engine"]
            save_data["turn_engine_state"] = {
                "ai_turns_in_a_row": getattr(te, "ai_turns_in_a_row", 0),
                "last_speaker": getattr(te, "last_speaker", None),
                "last_two_speakers": getattr(te, "last_two_speakers", []),
                "turn_count": getattr(te, "turn_count", 0),
                "interruption_count": getattr(te, "interruption_count", 0),
            }
            del save_data["turn_engine"]
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f)
    except Exception as e:
        print(f"Error saving session to tmp: {e}")

def load_session(s_id):
    if not s_id:
        return None
    if s_id in SESSIONS:
        return SESSIONS[s_id]
    try:
        tmp_path = os.path.join(tempfile.gettempdir(), f"gd_session_{s_id}.json")
        if os.path.exists(tmp_path):
            with open(tmp_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            te = TurnEngine()
            if "turn_engine_state" in data:
                tes = data["turn_engine_state"]
                te.ai_turns_in_a_row = tes.get("ai_turns_in_a_row", 0)
                te.last_speaker = tes.get("last_speaker")
                te.last_two_speakers = tes.get("last_two_speakers", [])
                te.turn_count = tes.get("turn_count", 0)
                te.interruption_count = tes.get("interruption_count", 0)
            data["turn_engine"] = te
            SESSIONS[s_id] = data
            return data
    except Exception as e:
        print(f"Error loading session from tmp: {e}")
    return None

def generate_llm_turn(persona, topic, mode, student_text, transcript, resume=None):
    system_instruction = persona["system_prompt"].format(topic=topic)
    recent_context = "\n".join([f"{t['name']}: {t['text']}" for t in transcript[-4:]])

    resume_context = ""
    if resume and resume.get("skills"):
        resume_context = f"\nCandidate Stated Resume Profile: Skills: [{', '.join(resume['skills'][:5])}], Projects: [{', '.join(resume.get('projects', [])[:2])}]"

    if mode == "interview":
        task_instruction = f"You are interviewing the candidate on '{topic}'. Critically analyze their statement, probe technical depth, or ask a sharp follow-up question related to architecture, scaling, or edge cases."
    else:
        task_instruction = f"You are participating in a fast-paced, high-stakes campus placement group discussion on '{topic}'. Actively debate what was just said: agree, disagree, introduce concrete examples, or challenge the candidate's premises in your unique persona style."

    prompt = f"""{system_instruction}
{resume_context}

Task: {task_instruction}

Recent Discussion Flow:
{recent_context}

Last Statement by Candidate: "{student_text}"

Respond as {persona['name']} in 1-2 spoken sentences (under 35 words). Be direct, conversational, and debate naturally. Never use markdown, bullet points, asterisks, or quotes:"""

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

    # 2. Secondary: Groq API
    if GROQ_KEY:
        try:
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
                data=json.dumps({
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}],
                    "max_tokens": 75,
                    "temperature": 0.7
                }).encode('utf-8')
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                text = res_json['choices'][0]['message']['content'].strip()
                return text.replace('*', '').replace('"', '').replace('\n', ' ')
        except Exception as e:
            print(f"Groq API fallback error: {e}")

    # 3. Fallback: OpenRouter
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

# Initialize Flask App
app = Flask(__name__, static_folder=DIRECTORY, static_url_path='')

@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        res = Response()
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return res

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    return response

# 1. Health endpoint
@app.route('/api/debug-dir', methods=['GET'])
def debug_dir():
    server_contents = []
    try:
        server_contents = os.listdir('/var/task/server')
    except Exception as e:
        server_contents = [str(e)]
    return jsonify({
        "DIRECTORY": DIRECTORY,
        "exists": os.path.exists(DIRECTORY),
        "server_contents": server_contents,
        "project_root": PROJECT_ROOT
    })

# 2. Session start endpoint
@app.route('/api/session/start', methods=['POST'])
@app.route('/session/start', methods=['POST'])
def session_start():
    payload = request.get_json(silent=True) or {}
    mode = payload.get('mode', 'gd')
    topic = payload.get('topic', 'Will Generative AI Replace Entry-Level Software Engineers?')
    panel_size = int(payload.get('panel_size', 4))
    s_id = str(uuid.uuid4())[:8]

    turn_engine = TurnEngine()
    resume_info = payload.get('resume', {})

    if mode == 'interview':
        skills_list = resume_info.get('skills', [])
        if skills_list:
            opening_text = f"Good morning. I am Ms. Kapoor. We have reviewed your resume highlighting {', '.join(skills_list[:3])}. We are evaluating candidates for our technical placement drive. Let us begin with your background and your approach to '{topic}'."
        else:
            opening_text = f"Good morning. I am Ms. Kapoor. We are evaluating candidates for our technical placement drive. Let us begin with your background and your approach to '{topic}'. Tell me about your practical experience."
        mod_key = "interviewer"
    else:
        opening_text = f"Good morning candidates. I am Mr. Verma, your moderator. All other participants are AI. Today's GD topic is: '{topic}'. You have 10 minutes. The floor is open."
        mod_key = "moderator"

    session_data = {
        "id": s_id,
        "mode": mode,
        "topic": topic,
        "panel_size": panel_size,
        "resume": resume_info,
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
    save_session(s_id, session_data)

    return jsonify({
        "session_id": s_id,
        "opening": opening_text,
        "speaker": mod_key,
        "moderator_voice": PERSONAS[mod_key]["voice"],
        "topic": topic
    })

# 3. Session inspect endpoint
@app.route('/api/session/<s_id>', methods=['GET'])
@app.route('/session/<s_id>', methods=['GET'])
def get_session(s_id):
    session = load_session(s_id)
    if session:
        # Avoid serialization error on TurnEngine
        clean_session = dict(session)
        if "turn_engine" in clean_session:
            clean_session["turn_engine"] = {
                "turn_count": getattr(clean_session["turn_engine"], "turn_count", 0),
                "ai_turns_in_a_row": getattr(clean_session["turn_engine"], "ai_turns_in_a_row", 0)
            }
        return jsonify(clean_session)
    return jsonify({"error": "Session not found"}), 404

# 4. Chat endpoint
@app.route('/api/chat', methods=['POST'])
@app.route('/chat', methods=['POST'])
def chat():
    payload = request.get_json(silent=True) or {}
    s_id = payload.get('session_id')
    student_text = payload.get('text', '').strip()
    interrupted = payload.get('interrupted', False)

    session = load_session(s_id)
    if not session:
        session = {
            "id": s_id or "temp",
            "mode": payload.get('mode', 'gd'),
            "topic": payload.get('topic', 'Technology & Campus Placements'),
            "turn_engine": TurnEngine(),
            "transcript": [],
            "interruptions": 0
        }
        save_session(session["id"], session)

    turn_engine = session["turn_engine"]

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

    next_spk = turn_engine.next_speaker(mode=session["mode"])
    persona = PERSONAS.get(next_spk, PERSONAS["aarav"])
    turn_engine.note_ai_spoke(next_spk)

    ai_text = generate_llm_turn(persona, session["topic"], session["mode"], student_text, session["transcript"], session.get("resume"))
    ai_text = re.sub(r'\[REJECT:.*?\]', '', ai_text).strip()

    session["transcript"].append({
        "id": len(session["transcript"]) + 1,
        "speaker": next_spk,
        "name": persona["name"],
        "role": persona["role"],
        "timestamp": payload.get('timestamp', '01:45'),
        "text": ai_text
    })

    save_session(session["id"], session)

    return jsonify({
        "speaker": next_spk,
        "persona": persona["name"],
        "role": persona["role"],
        "text": ai_text,
        "voice": persona["voice"],
        "rate": persona["rate"],
        "pitch": persona["pitch"],
        "color": persona["color"],
        "rejected": False
    })

# 5. TTS endpoint
@app.route('/api/tts', methods=['POST'])
@app.route('/tts', methods=['POST'])
def tts():
    silent_mp3 = b'ID3\x03\x00\x00\x00\x00\x0f\x00\x00\x00' + b'\xff\xfb\x90\x64\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' * 500
    try:
        payload = request.get_json(silent=True) or {}
        text = payload.get('text', 'Hello')
        speaker = payload.get('speaker', 'aarav')
        voice_choice = payload.get('voice_choice', 'voice1')

        persona = PERSONAS.get(speaker, PERSONAS["aarav"])
        voice_opts = persona.get("voice_options", {})
        selected_voice = voice_opts.get(voice_choice, persona["voice"])
        voice = payload.get('voice', selected_voice)
        rate = payload.get('rate', persona["rate"])
        pitch = payload.get('pitch', persona["pitch"])

        audio_bytes = None

        if HAS_EDGE_TTS and text:
            try:
                async def run_tts():
                    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
                    buf = io.BytesIO()
                    async for chunk in comm.stream():
                        if chunk['type'] == 'audio':
                            buf.write(chunk['data'])
                    return buf.getvalue()

                try:
                    audio_bytes = asyncio.run(run_tts())
                except Exception:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        audio_bytes = loop.run_until_complete(run_tts())
                    finally:
                        loop.close()
            except Exception as e_edge:
                print(f"Edge-TTS notice: {e_edge}")

        if not audio_bytes:
            audio_bytes = silent_mp3

        return Response(audio_bytes, mimetype='audio/mpeg', headers={'Content-Length': str(len(audio_bytes))})
    except Exception as ex:
        print(f"TTS endpoint error: {ex}")
        return Response(silent_mp3, mimetype='audio/mpeg', headers={'Content-Length': str(len(silent_mp3))})

# 6. Report endpoint
@app.route('/api/report', methods=['POST'])
@app.route('/report', methods=['POST'])
def report():
    payload = request.get_json(silent=True) or {}
    s_id = payload.get('session_id')
    session = load_session(s_id) or {}
    transcript = session.get('transcript', payload.get('transcript', []))
    topic = session.get('topic', 'Campus Placement Simulation')
    interruptions = session.get('interruptions', 0)

    stats = score_session_stats(transcript, interruptions)
    if session.get("rejected"):
        report_data = {
            "overall_score": 0.0,
            "tier": "Disqualified",
            "pass": False,
            "review_statement": f"Candidate was disqualified during the session. Reason: {session.get('reject_reason', 'Repeated off-topic or unprofessional statements (5 warnings exceeded).')}",
            "transcript": transcript,
            "stats": stats,
            "dimensions": {},
            "strengths": [],
            "weaknesses": [f"Session Auto-Terminated: {session.get('reject_reason', '5 Warnings Exceeded for conduct/relevance')}"],
            "red_flags": ["Professionalism Violation / Gibberish Detected. Session ended abruptly."],
            "missed_openings": [],
            "drills": ["Practice structured answering, professional debate boundaries, and active listening."]
        }
    else:
        mode = session.get('mode', payload.get('mode', 'gd'))
        report_data = generate_report_json(transcript, topic, stats, mode=mode)

    return jsonify(report_data)

# 7. Parse resume endpoint
@app.route('/api/parse-resume', methods=['POST'])
@app.route('/parse-resume', methods=['POST'])
def parse_resume():
    payload = request.get_json(silent=True) or {}
    resume_text = payload.get('text', '')
    jd_text = payload.get('jd_text', '')

    parsed = parse_resume_text(resume_text)
    if jd_text:
        parsed["jd_match"] = match_jd_skills(parsed["skills"], jd_text)

    return jsonify(parsed)

# 8. Generate placement topics endpoint
@app.route('/api/generate-topics', methods=['POST'])
@app.route('/generate-topics', methods=['POST'])
def generate_topics():
    payload = request.get_json(silent=True) or {}
    category = payload.get('category', 'Technology & Architecture')

    prompt = f"Generate 3 sharp, highly competitive campus placement Group Discussion topics for engineering candidates on '{category}'. Return ONLY a JSON array of 3 strings. No markdown, no numbers, no explanations."

    topics = [
        "Should AI Agents Have Autonomous Deployment Permissions in Production?",
        "Microservices Sprawl vs Monolith Simplicity for High-Velocity Startups",
        "Is Remote Work Weakening Junior Engineering Architecture Mentorship?"
    ]

    if GOOGLE_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={GOOGLE_KEY}"
            req = urllib.request.Request(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps({
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"maxOutputTokens": 100, "temperature": 0.8}
                }).encode('utf-8')
            )
            with urllib.request.urlopen(req, timeout=6) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                raw_text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
                raw_text = raw_text.replace('```json', '').replace('```', '').strip()
                parsed = json.loads(raw_text)
                if isinstance(parsed, list) and len(parsed) >= 2:
                    topics = parsed[:3]
        except Exception as e:
            print(f"Gemini topic generation fallback: {e}")

    return jsonify({"topics": topics})

# 9. Fallback Static Files router for local serving
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    if not path or path == '/':
        return send_from_directory(DIRECTORY, 'index.html')
    full_path = os.path.join(DIRECTORY, path)
    if os.path.exists(full_path) and not os.path.isdir(full_path):
        return send_from_directory(DIRECTORY, path)
    if os.path.exists(os.path.join(full_path, 'index.html')):
        return send_from_directory(full_path, 'index.html')
    return send_from_directory(DIRECTORY, 'index.html')
