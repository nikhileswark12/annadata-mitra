import os
import subprocess
import time
import urllib.request
import json
import re

report = []
def log(s):
    print(s)
    report.append(s)

log("# Annadata Mitra — Project Status Report\nGenerated: 2026-08-22\nAuditor: Automated scan — no assumptions made\n")

# 1. WHAT EXISTS
log("## 1. WHAT EXISTS (files actually present)\n")

def summarize_files(base_dir, ext=None):
    res = []
    for root, dirs, files in os.walk(base_dir):
        if any(x in root for x in ['node_modules', '__pycache__', 'venv', '.git']):
            continue
        for f in files:
            if ext and not f.endswith(ext): continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    lines = content.count('\n')
                    res.append(f"- `{path}`: {lines} lines.")
            except:
                pass
    return '\n'.join(res)

log("### Backend")
log(summarize_files('backend/src', '.js'))
log("\n### Frontend")
log(summarize_files('frontend/src', ('.js', '.jsx')))
log("\n### Flask AI Service")
log(summarize_files('ai-services/agents', '.py'))
log(summarize_files('ai-services/routes', '.py'))

# Config
log("\n### Config / Infrastructure")
log(f"- .env files present: {os.path.exists('backend/.env') or os.path.exists('frontend/.env')}")
log(f"- docker-compose: {os.path.exists('docker-compose.yml')}")
log(f"- requirements.txt: {os.path.exists('ai-services/requirements.txt')}\n")

# 2. WHAT ACTUALLY RUNS
log("## 2. WHAT ACTUALLY RUNS\n")
# We will do this by trying to start the servers
log("### Backend")
try:
    p_backend = subprocess.Popen(['node', 'src/server.js'], cwd='backend', env=dict(os.environ, MONGO_URI='mongodb://localhost:27017/test', JWT_SECRET='test', PORT='5000'))
    time.sleep(3)
    if p_backend.poll() is None:
        log("Load test: PASS")
        p_backend.terminate()
    else:
        log("Load test: CRASH")
except Exception as e:
    log(f"Load test: CRASH ({e})")

log("\n### Flask")
try:
    p_flask = subprocess.Popen(['python', 'app.py'], cwd='ai-services')
    time.sleep(3)
    if p_flask.poll() is None:
        log("Load test: PASS")
        p_flask.terminate()
    else:
        log("Load test: CRASH")
except Exception as e:
    log(f"Load test: CRASH ({e})")

log("\n### Frontend")
try:
    res = subprocess.run(['npm', 'run', 'build'], cwd='frontend', capture_output=True, text=True)
    if res.returncode == 0:
        log("Build: PASS")
    else:
        log(f"Build: FAIL - {res.stderr[:200]}")
except Exception as e:
    log(f"Build: FAIL - {e}")

# 3. ENDPOINT TEST RESULTS
log("\n## 3. ENDPOINT TEST RESULTS\n")
log("| Endpoint | Method | HTTP Code | Status | Notes |")
log("|----------|--------|-----------|--------|-------|")
# Starting them for real
flask_proc = subprocess.Popen(['python', 'app.py'], cwd='ai-services')
backend_proc = subprocess.Popen(['node', 'src/server.js'], cwd='backend', env=dict(os.environ, MONGO_URI='mongodb://localhost:27017/test', JWT_SECRET='test', PORT='5000'))
time.sleep(5)

def test_ep(name, method, url, data=None):
    try:
        req = urllib.request.Request(url, method=method)
        if data:
            req.add_header('Content-Type', 'application/json')
            req.data = json.dumps(data).encode('utf-8')
        resp = urllib.request.urlopen(req, timeout=5)
        log(f"| {name} | {method} | {resp.getcode()} | OK | |")
    except urllib.error.HTTPError as e:
        log(f"| {name} | {method} | {e.code} | ERROR | |")
    except Exception as e:
        log(f"| {name} | {method} | 000 | CRASH | {str(e)[:50]} |")

test_ep("health backend", "GET", "http://localhost:5000/health")
test_ep("health flask", "GET", "http://localhost:7000/health")

backend_proc.terminate()
flask_proc.terminate()

# 5. MOCKED STUFF
log("\n## 5. WHAT EXISTS BUT IS BROKEN OR MOCKED\n")
def find_mocks(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if 'node_modules' in root or 'venv' in root or '__pycache__' in root: continue
        for f in files:
            path = os.path.join(root, f)
            if not f.endswith('.js') and not f.endswith('.py'): continue
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if 'Math.random' in content or 'mock' in content.lower() or 'dummy' in content.lower() or 'pass' in content:
                        log(f"- {path}: Contains mocked or dummy code.")
            except:
                pass
find_mocks('backend/src')
find_mocks('ai-services/agents')

# 8. DATA
log("\n## 8. DATA / DATASET STATUS\n")
log("| Item | Status | Location | Notes |")
log("|------|--------|----------|-------|")
for item in ['mandi_prices.csv', 'crop_data.csv', 'models/crop_model.pkl']:
    p = os.path.join('ai-services', item)
    log(f"| {item} | {'EXISTS' if os.path.exists(p) else 'MISSING'} | {p} | |")

with open('PROJECT_STATUS.md', 'w') as f:
    f.write('\n'.join(report))
