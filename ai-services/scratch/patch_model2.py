import json
import zipfile
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(base_dir, "../models/vision/vision_model.keras")
dst = os.path.join(base_dir, "vision_model_patched.keras")

with zipfile.ZipFile(src, 'r') as zin:
    with zipfile.ZipFile(dst, 'w') as zout:
        for item in zin.infolist():
            if item.filename == 'config.json':
                s = zin.read(item.filename).decode('utf-8')
                s = s.replace('"keras.src.engine.functional"', '"keras.src.models.functional"')
                s = s.replace('"axis": [3]', '"axis": 3')
                # Replace for any other axis like [1], [2] if they exist
                s = s.replace('"axis": [1]', '"axis": 1')
                s = s.replace('"axis": [2]', '"axis": 2')
                zout.writestr(item, s)
            else:
                zout.writestr(item, zin.read(item.filename))
print("Patched successfully to", dst)
