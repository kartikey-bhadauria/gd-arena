import os
import sys

# Ensure root repository directory is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from server.app import app, PORT, GOOGLE_KEY, HAS_EDGE_TTS

def run_server():
    print(f"=====================================================")
    print(f" GD Arena Production Server Active: http://localhost:{PORT}")
    print(f" Google Gemini: {'READY' if GOOGLE_KEY else 'MISSING'}")
    print(f" Edge Neural TTS: {'ACTIVE' if HAS_EDGE_TTS else 'DISABLED'}")
    print(f" Design System: Primefold Light/Clean Theme")
    print(f"=====================================================")
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    run_server()
