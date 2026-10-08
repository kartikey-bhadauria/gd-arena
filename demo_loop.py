import urllib.request
import urllib.parse
import json
import time

BASE_URL = "https://gd-arena-phi.vercel.app"

def test_api():
    print("--- Starting GD Session Demo ---")
    
    # 1. Start Session
    req = urllib.request.Request(
        f"{BASE_URL}/api/session/start",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"mode": "gd", "topic": "Should AI Replace Software Engineers?", "panel_size": 4}).encode('utf-8')
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        session_id = data["session_id"]
        print(f"[START] Session created: {session_id}")
        print(f"[AI] {data['opening']}")

    # 2. Emulate 3 rounds of chat
    student_inputs = [
        "I believe AI will augment engineers, not replace them. We still need humans to handle edge cases and system architecture.",
        "But what about cost? Companies might prefer cheaper AI over expensive junior developers.",
        "That's a fair point, but someone still needs to verify that the AI's code is secure and optimized."
    ]

    for i, text in enumerate(student_inputs):
        print(f"\n--- Turn {i+1} ---")
        print(f"[STUDENT] {text}")
        
        # A. Send Chat
        chat_req = urllib.request.Request(
            f"{BASE_URL}/api/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"session_id": session_id, "text": text, "timestamp": f"0{i+1}:00"}).encode('utf-8')
        )
        with urllib.request.urlopen(chat_req, timeout=15) as chat_resp:
            chat_data = json.loads(chat_resp.read().decode('utf-8'))
            speaker = chat_data["speaker"]
            ai_text = chat_data["text"]
            voice = chat_data["voice"]
            print(f"[AI - {speaker}] {ai_text}")

        # B. Request TTS Audio
        tts_req = urllib.request.Request(
            f"{BASE_URL}/api/tts",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"text": ai_text, "voice": voice, "speaker": speaker}).encode('utf-8')
        )
        try:
            with urllib.request.urlopen(tts_req, timeout=15) as tts_resp:
                status = tts_resp.status
                audio_len = len(tts_resp.read())
                print(f"[TTS] Received {audio_len} bytes. Status: {status}")
        except urllib.error.HTTPError as e:
            print(f"[TTS FALLBACK] HTTP Error {e.code}: {e.reason} -> Browser would trigger SpeechSynthesis fallback!")
        
        time.sleep(1) # simulate short wait

    print("\n--- Generating Final Report ---")
    report_req = urllib.request.Request(
        f"{BASE_URL}/api/report",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"session_id": session_id}).encode('utf-8')
    )
    with urllib.request.urlopen(report_req, timeout=10) as report_resp:
        report_data = json.loads(report_resp.read().decode('utf-8'))
        print(f"[REPORT] Score: {report_data['overall_score']} | Pass: {report_data['pass']}")
        print(f"[REPORT] Review: {report_data['review_statement']}")

if __name__ == "__main__":
    test_api()
