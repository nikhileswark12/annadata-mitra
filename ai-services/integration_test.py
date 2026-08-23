
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
