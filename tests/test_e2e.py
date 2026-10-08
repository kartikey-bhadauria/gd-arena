import urllib.request
import urllib.parse
import json
import time

BASE_URL = "http://localhost:8000"

def test_get(path, expected_status=200):
    url = f"{BASE_URL}{path}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            assert resp.status == expected_status, f"Expected {expected_status}, got {resp.status}"
            return True, len(data)
    except Exception as e:
        return False, str(e)

def test_post_json(path, payload):
    url = f"{BASE_URL}{path}"
    try:
        req = urllib.request.Request(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload).encode('utf-8')
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            return True, json.loads(data.decode('utf-8'))
    except Exception as e:
        return False, str(e)

def run_all_tests():
    print("==================================================")
    print(" GD Arena Automated End-to-End Test Suite")
    print("==================================================")
    
    results = []

    # 1. Health check
    ok, data = test_get("/api/health")
    print(f"[{'PASS' if ok else 'FAIL'}] GET /api/health -> {data} bytes")
    results.append(ok)

    # 2. Static Pages
    pages = [
        "/",
        "/index.html",
        "/pages/login.html",
        "/pages/signup.html",
        "/pages/onboarding.html",
        "/pages/resume-upload.html",
        "/pages/mode-select.html",
        "/pages/gd-room.html",
        "/pages/interview-room.html",
        "/pages/report.html",
        "/pages/history.html",
        "/demo.html"
    ]
    for p in pages:
        ok, size = test_get(p)
        print(f"[{'PASS' if ok else 'FAIL'}] GET {p} -> {size} bytes")
        results.append(ok)

    # 3. Static JS & CSS Assets
    assets = [
        "/css/style.css",
        "/js/config.js",
        "/js/api.js",
        "/js/auth.js",
        "/js/landing.js",
        "/js/onboarding.js",
        "/js/resume.js",
        "/js/stt.js",
        "/js/tts.js",
        "/js/vu-meter.js",
        "/js/turn-manager.js",
        "/js/room.js",
        "/js/report.js"
    ]
    for a in assets:
        ok, size = test_get(a)
        print(f"[{'PASS' if ok else 'FAIL'}] GET {a} -> {size} bytes")
        results.append(ok)

    # 4. Resume Parsing & JD Match API
    ok, res = test_post_json("/api/parse-resume", {
        "text": "Kartikey Bhadauria\\nB.Tech CSE\\nSkills: Python, FastAPI, React, Docker, SQL\\nProjects: GD Arena voice-first multi-agent platform",
        "jd_text": "Looking for Backend Engineer proficient in Python, FastAPI, Docker, and Microservices."
    })
    print(f"[{'PASS' if ok else 'FAIL'}] POST /api/parse-resume -> Skills: {res.get('skills', [])}, JD Score: {res.get('jd_match', {}).get('score')}%")
    results.append(ok)

    # 5. Start GD Session API
    ok, s_data = test_post_json("/api/session/start", {
        "mode": "gd",
        "topic": "Should AI Replace Entry-Level Software Engineers in Campus Hiring?",
        "panel_size": 4
    })
    session_id = s_data.get("session_id")
    print(f"[{'PASS' if ok else 'FAIL'}] POST /api/session/start -> Session ID: {session_id}, Opening: {s_data.get('opening', '')[:45]}...")
    results.append(ok)

    # 6. Chat Dialogue Turn API
    ok, chat_data = test_post_json("/api/chat", {
        "session_id": session_id,
        "text": "AI models generate code quickly, but human engineers are required for edge cases and security review.",
        "timestamp": "01:20"
    })
    print(f"[{'PASS' if ok else 'FAIL'}] POST /api/chat -> {chat_data.get('persona')}: \"{chat_data.get('text')}\"")
    results.append(ok)

    # 7. Neural TTS Audio API
    try:
        tts_req = urllib.request.Request(
            f"{BASE_URL}/api/tts",
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "text": "That is a valid point. Let us analyze the security trade-offs.",
                "speaker": "rohan",
                "voice_choice": "voice1",
                "engine": "edge"
            }).encode('utf-8')
        )
        with urllib.request.urlopen(tts_req, timeout=8) as tts_resp:
            audio_bytes = tts_resp.read()
            ok_tts = (tts_resp.status == 200 and len(audio_bytes) > 5000)
            print(f"[{'PASS' if ok_tts else 'FAIL'}] POST /api/tts -> Audio stream received: {len(audio_bytes)} bytes")
            results.append(ok_tts)
    except Exception as e:
        print(f"[FAIL] POST /api/tts -> Error: {e}")
        results.append(False)

    # 8. Report Generation API
    ok, rep_data = test_post_json("/api/report", {
        "session_id": session_id
    })
    print(f"[{'PASS' if ok else 'FAIL'}] POST /api/report -> Score: {rep_data.get('overall_score')}/10, Tier: {rep_data.get('tier')}, Pass: {rep_data.get('pass')}")
    results.append(ok)

    # Final Summary
    passed_count = sum(1 for r in results if r)
    total_count = len(results)
    print("==================================================")
    print(f" Test Results: {passed_count}/{total_count} Passed ({int(passed_count/total_count*100)}%)")
    print("==================================================")

if __name__ == '__main__':
    run_all_tests()
