
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
