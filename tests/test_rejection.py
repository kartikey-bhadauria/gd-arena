import urllib.request
import json

BASE_URL = "http://localhost:8000"

# 1. Start Session
s_req = urllib.request.Request(
    f"{BASE_URL}/api/session/start",
    headers={"Content-Type": "application/json"},
    data=json.dumps({"mode": "interview", "topic": "Distributed Architecture"}).encode('utf-8')
)
with urllib.request.urlopen(s_req) as resp:
    s_data = json.loads(resp.read().decode('utf-8'))
    session_id = s_data['session_id']

# 2. Chat with complete rubbish / off-topic nonsense
chat_req = urllib.request.Request(
    f"{BASE_URL}/api/chat",
    headers={"Content-Type": "application/json"},
    data=json.dumps({
        "session_id": session_id,
        "text": "asdfasdf banana monkey spaceship bla bla bla I want to eat apples lalala 12345",
        "timestamp": "01:00"
    }).encode('utf-8')
)
with urllib.request.urlopen(chat_req) as resp:
    chat_res = json.loads(resp.read().decode('utf-8'))
    print("AI Reply:", chat_res.get("text"))
    print("Rejected Flag:", chat_res.get("rejected"))

# 3. Check Report
rep_req = urllib.request.Request(
    f"{BASE_URL}/api/report",
    headers={"Content-Type": "application/json"},
    data=json.dumps({"session_id": session_id}).encode('utf-8')
)
with urllib.request.urlopen(rep_req) as resp:
    rep_res = json.loads(resp.read().decode('utf-8'))
    print("Report Overall Score:", rep_res.get("overall_score"))
    print("Report Tier:", rep_res.get("tier"))
    print("Report Weaknesses / Reason:", rep_res.get("weaknesses"))
