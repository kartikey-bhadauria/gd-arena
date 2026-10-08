import os
import shutil

root = os.path.abspath(os.path.dirname(__file__))
server_dir = os.path.join(root, 'server')
templates_dir = os.path.join(server_dir, 'templates')
pages_template_dir = os.path.join(templates_dir, 'pages')
static_dir = os.path.join(server_dir, 'static')

os.makedirs(pages_template_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

public_dir = os.path.join(root, 'public')
if not os.path.exists(public_dir):
    public_dir = os.path.join(server_dir, 'public')

if os.path.exists(public_dir):
    for root_w, dirs, files in os.walk(public_dir):
        for f in files:
            src = os.path.join(root_w, f)
            rel = os.path.relpath(src, public_dir)
            if f.endswith('.html'):
                if 'pages' in rel.lower() or 'pages' in root_w.lower():
                    dest = os.path.join(pages_template_dir, f)
                else:
                    dest = os.path.join(templates_dir, f)
                shutil.copy2(src, dest)
            else:
                dest = os.path.join(static_dir, rel.replace('\\', '/'))
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src, dest)

print("Standard Flask templates and static layout organized successfully!")
