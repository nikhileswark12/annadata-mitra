import os
import sys
import subprocess
import json
import re
import time
import urllib.request
import urllib.error

def run_cmd(cmd, cwd=None, env=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, env=env, shell=True, capture_output=True, text=True)
        return res.stdout + res.stderr
    except Exception as e:
        return str(e)

def get_file_list(base_dir, exclude_dirs):
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in filenames:
            files.append(os.path.join(root, f).replace("\\", "/"))
    return sorted(files)

def get_1line_desc(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if filepath.endswith('.js') or filepath.endswith('.jsx'):
                classes = re.findall(r'class\s+(\w+)', content)
                funcs = re.findall(r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)', content)
                funcs = [f[0] or f[1] for f in funcs if f[0] or f[1]]
                routes = re.findall(r'router\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]', content)
                desc = []
                if classes: desc.append(f"Classes: {', '.join(classes[:3])}")
                if routes: desc.append(f"Routes: {', '.join(r[1] for r in routes[:3])}")
                if funcs: desc.append(f"Functions: {', '.join(funcs[:3])}")
                return " | ".join(desc) if desc else "Utility/Config file"
            elif filepath.endswith('.py'):
                classes = re.findall(r'class\s+(\w+)', content)
                funcs = re.findall(r'def\s+(\w+)', content)
                routes = re.findall(r'@.*\.route\([\'"]([^\'"]+)[\'"]', content)
                desc = []
                if classes: desc.append(f"Classes: {', '.join(classes[:3])}")
                if routes: desc.append(f"Routes: {', '.join(routes[:3])}")
                if funcs: desc.append(f"Functions: {', '.join(funcs[:3])}")
                return " | ".join(desc) if desc else "Script/Utility file"
    except:
        pass
    return "Unknown"

# 1. Inventory
backend_files = get_file_list('backend/src', ['node_modules', '__pycache__', '.git', 'dist', 'build', 'uploads', 'logs', 'models', 'datasets'])
frontend_files = get_file_list('frontend/src', ['node_modules', '__pycache__', '.git', 'dist', 'build', 'uploads', 'logs', 'models', 'datasets'])
flask_files = get_file_list('ai-services', ['node_modules', '__pycache__', '.git', 'dist', 'build', 'uploads', 'logs', 'models', 'datasets', 'venv'])

# 2. Package Versions
node_audit_script = """
const fs = require('fs');
if (!fs.existsSync('./package.json')) { console.log('No package.json'); process.exit(0); }
const pkg = require('./package.json');
const all = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
const critical = process.argv.slice(2);
critical.forEach(p => {
  const v = all[p];
  if (!v) console.log(`MISSING: ${p}`);
  else console.log(`OK: ${p} (${v})`);
});
"""
with open('backend/audit_node.js', 'w') as f: f.write(node_audit_script)
with open('frontend/audit_node.js', 'w') as f: f.write(node_audit_script)

backend_deps = run_cmd('node audit_node.js dotenv express mongoose bcryptjs jsonwebtoken multer cors helmet express-validator express-rate-limit axios uuid compression xss-clean express-mongo-sanitize', cwd='backend')
frontend_deps = run_cmd('node audit_node.js vite @vitejs/plugin-react react react-router-dom axios @mui/material chart.js', cwd='frontend')

py_audit_script = """
import importlib
packages = {
  'flask': 'flask', 'flask_cors': 'flask_cors', 'pandas': 'pandas',
  'sklearn': 'scikit-learn', 'numpy': 'numpy', 'joblib': 'joblib',
  'PIL': 'pillow', 'dotenv': 'python-dotenv', 'scipy': 'scipy', 'statsmodels': 'statsmodels'
}
for mod, pkg in packages.items():
    try:
        m = importlib.import_module(mod)
        v = getattr(m, '__version__', 'unknown')
        print(f'OK: {pkg} ({v})')
    except ImportError:
        print(f'MISSING: {pkg}')
"""
with open('ai-services/audit_py.py', 'w') as f: f.write(py_audit_script)
flask_deps = run_cmd('python audit_py.py', cwd='ai-services')

# 3. Backend Load Test
backend_load_script = """
process.env.MONGO_URI='mongodb://localhost:27017/test';
process.env.JWT_SECRET='annadata_mitra_super_secret_jwt_key_2025_parul_university';
process.env.PYTHON_SERVICE_URL='http://localhost:7000';
process.env.FRONTEND_URL='http://localhost:5173';
process.env.NODE_ENV='development';
process.env.PORT='5000';
try {
  const app = require('./src/app');
  app._router.stack.filter(r => r.route).forEach(r => console.log(Object.keys(r.route.methods)[0].toUpperCase(), r.route.path));
  app._router.stack.filter(r => r.name === 'router').forEach(r => r.handle.stack.filter(s => s.route).forEach(s => console.log(Object.keys(s.route.methods)[0].toUpperCase(), s.route.path)));
  console.log('OK: app.js loads without crash');
} catch(e) {
  console.log('CRASH:', e.message);
}
"""
with open('backend/load_test.js', 'w') as f: f.write(backend_load_script)
backend_load_out = run_cmd('node load_test.js', cwd='backend')

# 4. Flask Load Test
flask_load_script = """
import sys, traceback
sys.path.insert(0, '.')
modules = []
for mod in ['data.crop_knowledge','data.weather_knowledge', 'data.disease_knowledge','data.market_knowledge']:
    try: __import__(mod, fromlist=['']); print(f'OK: {mod}')
    except Exception as e: print(f'CRASH: {mod} - {e}')
for mod in ['agents.base_agent','agents.crop_agent','agents.weather_agent', 'agents.vision_agent','agents.market_agent','agents.strategist_agent']:
    try: __import__(mod, fromlist=['']); print(f'OK: {mod}')
    except Exception as e: print(f'CRASH: {mod} - {e}')
for mod in ['routes.crop_routes','routes.weather_routes','routes.vision_routes', 'routes.market_routes','routes.strategist_routes']:
    try: __import__(mod, fromlist=['']); print(f'OK: {mod}')
    except Exception as e: print(f'CRASH: {mod} - {e}')
try:
    from app import app
    print('OK: app.py imports')
except Exception as e:
    print(f'CRASH: app.py - {e}')
"""
with open('ai-services/load_test.py', 'w') as f: f.write(flask_load_script)
flask_load_out = run_cmd('python load_test.py', cwd='ai-services')

# 5. Flask Integration Test
flask_test_script = r"""
import json, io, sys, traceback
sys.path.insert(0, '.')
from app import app
client = app.test_client()
passed = failed = 0

def ok(name, condition, detail=''):
    global passed, failed
    if condition:
        print(f'  PASS: {name}')
        passed += 1
    else:
        print(f'  FAIL: {name} - {detail}')
        failed += 1

print('[HEALTH]')
try:
    r = client.get('/health')
    d = json.loads(r.data)
    ok('status 200', r.status_code == 200, r.status_code)
    ok('status=success', d.get('status') == 'success', d)
except Exception as e:
    print(f'  CRASH: {e}'); failed += 1

print('[CROP]')
try:
    payload = {'nitrogen':90,'phosphorus':42,'potassium':43,'ph':6.5,'rainfall':202,'temperature':25,'humidity':82}
    r = client.post('/crop-recommend', data=json.dumps(payload), content_type='application/json')
    d = json.loads(r.data)
    ok('200', r.status_code == 200, r.status_code)
except Exception as e: print(f'  CRASH: {e}'); failed += 1

print('[WEATHER]')
try:
    r = client.post('/weather-risk', data=json.dumps({'location':'Vadodara, Gujarat','crop':'rice'}), content_type='application/json')
    d = json.loads(r.data)
    ok('200', r.status_code == 200, r.status_code)
except Exception as e: print(f'  CRASH: {e}'); failed += 1

print('[VISION]')
try:
    fake_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' + b'\x00'*200
    r = client.post('/disease-detect', data={'image': (io.BytesIO(fake_png), 'leaf.png', 'image/png')}, content_type='multipart/form-data')
    d = json.loads(r.data)
    ok('200', r.status_code == 200, r.status_code)
except Exception as e: print(f'  CRASH: {e}'); failed += 1

print('[MARKET]')
try:
    r = client.post('/market-insights', data=json.dumps({'crop':'Rice','location':'Vadodara, Gujarat','quantity':'500'}), content_type='application/json')
    d = json.loads(r.data)
    ok('200', r.status_code == 200, r.status_code)
except Exception as e: print(f'  CRASH: {e}'); failed += 1

print('[STRATEGIST]')
try:
    r = client.post('/strategist-generate', data=json.dumps({'goal':'I want to maximize rice income in Gujarat this Kharif season'}), content_type='application/json')
    d = json.loads(r.data)
    ok('200', r.status_code == 200, r.status_code)
except Exception as e: print(f'  CRASH: {e}'); failed += 1

print(f'RESULTS: {passed} passed, {failed} failed out of {passed+failed} tests')
"""
with open('ai-services/integration_test.py', 'w') as f: f.write(flask_test_script)
flask_test_out = run_cmd('python integration_test.py', cwd='ai-services')

# 6. Frontend Audit
frontend_build = run_cmd('npm run build', cwd='frontend')
localstorage_keys = run_cmd('findstr /S /R "localStorage\.\(setItem\|getItem\|removeItem\)" frontend\\src\\* | findstr /V "token user"', shell=True)

# 7. Live Server Test
print("Starting servers...")
flask_proc = subprocess.Popen('python app.py', cwd='ai-services', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
backend_proc = subprocess.Popen('npm start', cwd='backend', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(10)

live_test_script = """
import urllib.request
import json
import jwt
try:
    token = jwt.encode({"id": "507f1f77bcf86cd799439011"}, "annadata_mitra_super_secret_jwt_key_2025_parul_university", algorithm="HS256")
except Exception as e:
    token = "ERROR"

results = []
def check(url, payload=None, expect=200):
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {token}')
    if payload:
        req.add_header('Content-Type', 'application/json')
        req.data = json.dumps(payload).encode('utf-8')
    try:
        resp = urllib.request.urlopen(req)
        results.append(f"PASS: {url} -> HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        results.append(f"FAIL: {url} -> HTTP {e.code} expected {expect}")
    except Exception as e:
        results.append(f"FAIL: {url} -> {e}")

check("http://localhost:5000/health")
check("http://localhost:5000/api/crop/recommend", {"nitrogen":90,"phosphorus":42,"potassium":43,"ph":6.5,"rainfall":202,"temperature":25,"humidity":82,"location":"Vadodara"})
check("http://localhost:5000/api/weather/risk", {"location":"Vadodara, Gujarat"})
check("http://localhost:5000/api/market/insights", {"crop":"Rice","location":"Vadodara, Gujarat","quantity":"500"})
check("http://localhost:5000/api/strategist/generate", {"goal":"Maximize rice income Gujarat Kharif season"})

print("\\n".join(results))
"""
with open('live_test.py', 'w') as f: f.write(live_test_script)
live_test_out = run_cmd('python live_test.py')

flask_proc.terminate()
backend_proc.terminate()

with open('SCAN_REPORT.md', 'w', encoding='utf-8') as f:
    f.write("# Annadata Mitra - Repository Scan Report\\n")
    f.write("Generated: 2026-08-09\\n\\n")
    f.write("## 1. File Inventory\\n### Backend (src/)\\n")
    for b in backend_files: f.write(f"- {b}: {get_1line_desc(b)}\\n")
    f.write("\\n### Frontend (src/)\\n")
    for fr in frontend_files: f.write(f"- {fr}: {get_1line_desc(fr)}\\n")
    f.write("\\n### Flask (ai-services/)\\n")
    for fl in flask_files: f.write(f"- {fl}: {get_1line_desc(fl)}\\n")
    
    f.write("\\n## 2. Package Versions\\n### Backend\\n```\\n")
    f.write(backend_deps)
    f.write("```\\n### Frontend\\n```\\n")
    f.write(frontend_deps)
    f.write("```\\n### Python\\n```\\n")
    f.write(flask_deps)
    f.write("```\\n\\n")
    
    f.write("## 4. Flask Agent Status\\n```\\n")
    f.write(flask_load_out)
    f.write("```\\n\\n")
    
    f.write("## 5. Flask Test Results\\n```\\n")
    f.write(flask_test_out)
    f.write("```\\n\\n")
    
    f.write("## 6. Backend Route Coverage\\n```\\n")
    f.write(backend_load_out)
    f.write("```\\n\\n")
    
    f.write("## 8. Live Server Test Results\\n```\\n")
    f.write(live_test_out)
    f.write("```\\n")

print("Report generated.")
