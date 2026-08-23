
import sys; sys.path.insert(0, '.')
for a in ['crop','weather','vision','market','strategist']:
  try: __import__(f'agents.{a}_agent', fromlist=['']); print(f'{a}:OK')
  except Exception as e: print(f'{a}:CRASH')
