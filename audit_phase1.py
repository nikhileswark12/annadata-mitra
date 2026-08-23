import os
import subprocess
import json
import re

IGNORE_DIRS = ['node_modules', '__pycache__', '.git', 'dist', 'build', 'uploads', 'logs']

def get_files():
    all_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            all_files.append(os.path.join(root, f))
    return sorted(all_files)

files = get_files()

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {path}: {e}"

with open('audit_report.txt', 'w', encoding='utf-8') as report:
    report.write("====== FULL FILE TREE ======\n")
    report.write('\n'.join(files) + '\n\n')
    
    report.write("====== PACKAGE.JSON FILES ======\n")
    for f in files:
        if f.endswith('package.json'):
            report.write(f"--- {f} ---\n{read_file(f)}\n\n")

    report.write("====== PYTHON REQUIREMENTS ======\n")
    for f in files:
        if f.endswith('requirements.txt'):
            report.write(f"--- {f} ---\n{read_file(f)}\n\n")

    report.write("====== ENV FILES ======\n")
    for f in files:
        if f.endswith('.env') or f.endswith('.env.local') or f.endswith('.env.example'):
            report.write(f"--- {f} ---\n{read_file(f)}\n\n")

    report.write("====== DOCKER FILES ======\n")
    for f in files:
        if 'Dockerfile' in f or 'docker-compose' in f:
            report.write(f"--- {f} ---\n{read_file(f)}\n\n")
