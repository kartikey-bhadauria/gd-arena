import urllib.request
import json
import time

BASE_URL = "http://localhost:8000"

# 1. Start Session
s_req = urllib.request.Request(
    f"{BASE_URL}/api/session/start",
    headers={"Content-Type": "application/json"},
    data=json.dumps({"mode": "interview", "topic": "Distributed Microservices Architecture"}).encode('utf-8')
)
with urllib.request.urlopen(s_req) as resp:
    s_data = json.loads(resp.read().decode('utf-8'))
    session_id = s_data['session_id']

print(f"Session started: {session_id}")

# 2. Issue 5 consecutive rubbish statements to trigger 5 warnings and auto-disqualification
for i in range(1, 6):
    chat_req = urllib.request.Request(
        f"{BASE_URL}/api/chat",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "session_id": session_id,
            "text": f"nonsense rubbish gibberish bla bla round {i}",
            "timestamp": f"0{i}:00"
        }).encode('utf-8')
    )
    with urllib.request.urlopen(chat_req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print(f"Turn {i} -> Warnings: {res.get('warnings')}/5 | Rejected: {res.get('rejected')}")
        print(f"        AI Reply: {res.get('text')}")

# 3. Verify final report with transcript log and final review statement
rep_req = urllib.request.Request(
    f"{BASE_URL}/api/report",
    headers={"Content-Type": "application/json"},
    data=json.dumps({"session_id": session_id}).encode('utf-8')
)
with urllib.request.urlopen(rep_req) as resp:
    rep = json.loads(resp.read().decode('utf-8'))
    print("\n--- Final Scorecard & Review ---")
    print("Overall Score:", rep.get("overall_score"))
    print("Tier:", rep.get("tier"))
    print("Review Statement:", rep.get("review_statement"))
    print(f"Transcript Turns Recorded: {len(rep.get('transcript', []))}")
