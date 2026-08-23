import shutil
import zipfile
import json
import os

base_dir = "f:/Annadata Mitra/annadata-mitra/ai-services"
src = os.path.join(base_dir, "models/vision/vision_model.keras")
dst = os.path.join(base_dir, "scratch/vision_model_patched.keras")

shutil.copy(src, dst)

def fix_config(config):
    if isinstance(config, dict):
        for k, v in config.items():
            if k == 'axis' and isinstance(v, list) and len(v) > 0:
                config[k] = v[0]
            elif isinstance(v, (dict, list)):
                fix_config(v)
    elif isinstance(config, list):
        for item in config:
            fix_config(item)

# extract, modify, zip again
with zipfile.ZipFile(src, 'r') as zin:
    with zipfile.ZipFile(dst, 'w') as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'config.json':
                config_str = data.decode('utf-8')
                # Also fix the engine.functional -> models.functional error
                config_str = config_str.replace("keras.src.engine.functional", "keras.src.models.functional")
                config = json.loads(config_str)
                fix_config(config)
                data = json.dumps(config).encode('utf-8')
            zout.writestr(item, data)

print("Patched!")
