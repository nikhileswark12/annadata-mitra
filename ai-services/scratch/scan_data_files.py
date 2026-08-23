import os
import json
import sys

base_dir = "f:/Annadata Mitra/annadata-mitra"
extensions = {".csv", ".xlsx", ".xls", ".json", ".parquet", ".geojson", ".tif", ".tiff", ".jpg", ".jpeg", ".png", ".xml", ".zip", ".txt", ".npz", ".npy"}
ignore_dirs = {"node_modules", "venv", "__pycache__", "build", "cache", ".git", "experiments"}

file_list = []

for root, dirs, files in os.walk(base_dir):
    dirs[:] = [d for d in dirs if d not in ignore_dirs and "cache" not in d.lower()]
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in extensions:
            path = os.path.join(root, f)
            size = os.path.getsize(path)
            file_list.append({"path": path.replace(base_dir, "").lstrip("\\/"), "ext": ext, "size": size})

with open("scratch/data_files.json", "w") as out:
    json.dump(file_list, out, indent=2)

print(f"Found {len(file_list)} files.")
