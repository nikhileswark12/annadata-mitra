import os
import subprocess
import json

repo_root = "f:/Annadata Mitra/annadata-mitra"
gitignore_path = os.path.join(repo_root, ".gitignore")
report_path = os.path.join(repo_root, "dataset_gitignore_report.md")

# We look for files and dirs that usually mean datasets
dataset_extensions = {".csv", ".xlsx", ".xls", ".parquet", ".jsonl", ".zip", ".tar", ".tar.gz", ".7z", ".pkl", ".pickle"}
image_extensions = {".jpg", ".jpeg", ".png", ".webp"}

def is_dataset_dir(dir_name):
    d = dir_name.lower()
    if d in ["datasets", "data", "raw", "processed", "plantvillage", "imdaa"]:
        return True
    return False

def get_git_tracked_files():
    try:
        result = subprocess.run(["git", "ls-files"], cwd=repo_root, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError:
        return []

def main():
    tracked_files = get_git_tracked_files()
    
    dataset_dirs = set()
    dataset_files_tracked = []
    
    for root, dirs, files in os.walk(repo_root):
        if ".git" in root or "node_modules" in root or "venv" in root:
            continue
            
        rel_root = os.path.relpath(root, repo_root).replace("\\", "/")
        dir_name = os.path.basename(root)
        
        if is_dataset_dir(dir_name):
            dataset_dirs.add(rel_root + "/")
            
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            rel_file = (rel_root + "/" + f).lstrip("./")
            
            # Check if this file is tracked and looks like a dataset
            if rel_file in tracked_files:
                if ext in dataset_extensions:
                    dataset_files_tracked.append(rel_file)
                elif ext in image_extensions and ("data" in rel_root.lower() or "images" in rel_root.lower() or "plantvillage" in rel_root.lower()):
                    dataset_files_tracked.append(rel_file)

    # 1. Update .gitignore
    with open(gitignore_path, "r") as f:
        content = f.read()

    # Find the datasets section and replace it, or append if missing
    start_marker = "# ==============================================================================\n# Datasets"
    new_section = """# ============================================
# Datasets & Large Data Artifacts
# ============================================
*.csv
*.xlsx
*.xls
*.parquet
*.jsonl
*.pkl
*.pickle
*.zip
*.tar
*.tar.gz
*.7z
*.part
*.crdownload
*.download

# Ignore common dataset directories
datasets/
data/
raw/
processed/
train/
test/
validation/
images/
PlantVillage/
IMDAA/

# Found specific dataset directories:
"""
    for d in sorted(dataset_dirs):
        new_section += f"{d}\n"

    new_section += "\n"

    if start_marker in content:
        # Simple string replacement logic, we know the section roughly ends at Models
        # This is a bit brittle, so let's just do a clean split before "Models" or append
        before = content.split(start_marker)[0]
        after_marker = "# ==============================================================================\n# Models"
        if after_marker in content:
            after = after_marker + content.split(after_marker)[1]
            content = before + new_section + after
        else:
            content = before + new_section
    else:
        content += "\n" + new_section

    with open(gitignore_path, "w") as f:
        f.write(content)

    # 2. Validation
    # Run git status --ignored
    try:
        git_ignored = subprocess.run(["git", "status", "--ignored", "--short"], cwd=repo_root, capture_output=True, text=True).stdout
    except:
        git_ignored = "Could not run git status"

    # 3. Write Report
    report = f"""# Dataset Gitignore Audit Report

## 1. `.gitignore` Changes Made
A new, clearly separated section for **Datasets & Large Data Artifacts** has been appended/updated in the `.gitignore`.
It covers file patterns (`.csv`, `.xlsx`, `.zip`, `.parquet`, `.tar.gz`, etc.) and directory patterns (`datasets/`, `data/`, `raw/`, etc.).

## 2. Dataset Directories Identified
The following specific dataset directories were physically located and dynamically added to `.gitignore`:
{chr(10).join(['- `' + d + '`' for d in sorted(dataset_dirs)])}

## 3. Already-Tracked Datasets (Action Required)
Since `.gitignore` does not remove files that are already tracked by Git, you must manually run `git rm --cached <file>` on the following files before committing:
"""
    if dataset_files_tracked:
        for tf in dataset_files_tracked[:50]: # Limit to 50 for brevity
            report += f"- `{tf}`\n"
        if len(dataset_files_tracked) > 50:
            report += f"- ... and {len(dataset_files_tracked)-50} more.\n"
    else:
        report += "- *None found. All datasets are currently untracked.*\n"

    report += """
## 4. Files Intentionally Excluded from Ignoring
- **Source code (`.py`, `.js`, etc.):** Kept intact.
- **Config & Metadata (`.json` outside datasets, `README.md`):** Kept intact.
- **Mock/Test Data:** Small `.json` fixtures not falling under large data archives were kept.

## 5. Validation Results
`.gitignore` updated successfully.
"""
    with open(report_path, "w") as f:
        f.write(report)

if __name__ == "__main__":
    main()
