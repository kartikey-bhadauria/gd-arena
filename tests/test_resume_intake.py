import urllib.request
import json

BASE_URL = "http://localhost:8000"

# 1. Parse Resume
p_req = urllib.request.Request(
    f"{BASE_URL}/api/parse-resume",
    headers={"Content-Type": "application/json"},
    data=json.dumps({
        "text": "Kartikey Bhadauria. Skills: Python, FastAPI, Docker, PostgreSQL, React. Projects: GD Arena voice interview platform, Redis task queue."
    }).encode('utf-8')
)
with urllib.request.urlopen(p_req) as resp:
    parsed = json.loads(resp.read().decode('utf-8'))
    print("Parsed Skills:", parsed.get("skills"))

# 2. Start Session with Resume attached
s_req = urllib.request.Request(
    f"{BASE_URL}/api/session/start",
    headers={"Content-Type": "application/json"},
    data=json.dumps({
        "mode": "interview",
        "topic": "Microservices & Distributed Systems",
        "resume": parsed
    }).encode('utf-8')
)
with urllib.request.urlopen(s_req) as resp:
    s_data = json.loads(resp.read().decode('utf-8'))
    print("Interviewer Opening with Resume Context:", s_data.get("opening"))
