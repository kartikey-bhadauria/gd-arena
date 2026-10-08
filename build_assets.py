import os
import json
import base64

public_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "public"))
if not os.path.exists(public_dir):
    public_dir = os.path.abspath(os.path.join(os.getcwd(), "public"))

assets = {}
if os.path.exists(public_dir):
    for root, dirs, files in os.walk(public_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, public_dir).replace('\\', '/')
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                assets[rel_path] = {'type': 'text', 'content': content}
            except Exception:
                with open(full_path, 'rb') as f:
                    content_bytes = f.read()
                assets[rel_path] = {'type': 'binary', 'content': base64.b64encode(content_bytes).decode('utf-8')}

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "server", "static_assets.py"))
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# Auto-generated static assets bundle for Vercel serverless reliability\n')
    f.write('STATIC_ASSETS = ' + json.dumps(assets, indent=2))

print(f"Generated static assets bundle with {len(assets)} files at {out_path}!")
