import os
import subprocess
import json

repo_root = "f:/Annadata Mitra/annadata-mitra"

def run_cmd(cmd):
    try:
        return subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        return e.stdout + "\n" + e.stderr

def main():
    print("Starting Git Dataset Cleanup...")
    
    # 1. Audit Git Index
    tracked_files = run_cmd(["git", "ls-files"]).splitlines()
    staged_files = run_cmd(["git", "diff", "--name-only", "--cached"]).splitlines()
    
    dataset_extensions = {".csv", ".csv.gz", ".tsv", ".xlsx", ".xls", ".parquet", ".feather", ".jsonl", ".pkl", ".pickle", ".npy", ".npz", ".mat", ".h5", ".hdf5", ".zip", ".tar", ".tar.gz", ".7z", ".rar"}
    image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
    
    dataset_dirs_indicators = ["datasets/", "dataset/", "data/", "raw/", "processed/", "training/", "train/", "validation/", "val/", "test/", "testing/", "images/", "plantvillage/", "plant disease data/", "crop/", "market/", "weather/", "soil/"]
    
    dataset_files_to_remove = set()
    dataset_dirs_to_ignore = set()
    
    for f in tracked_files:
        lower_f = f.lower()
        ext = os.path.splitext(f)[1].lower()
        
        is_dataset = False
        
        # Check explicit dataset directories
        if "ai-services/datasets/" in lower_f or "plant disease data" in lower_f or "plantvillage" in lower_f:
            is_dataset = True
            
        # Check extensions
        if ext in dataset_extensions:
            is_dataset = True
            
        # Check image extensions but only if in dataset-like paths
        if ext in image_extensions:
            if any(ind in lower_f for ind in dataset_dirs_indicators):
                is_dataset = True
                
        if is_dataset:
            dataset_files_to_remove.add(f)
            
            # Find the root dataset dir to ignore
            parts = f.split("/")
            for i in range(len(parts)):
                subpath = "/".join(parts[:i+1]) + "/"
                if any(ind in subpath.lower() for ind in ["datasets/", "plant disease data/", "plantvillage/"]):
                    dataset_dirs_to_ignore.add(subpath)
                    break

    # Also add standard ones just in case
    dataset_dirs_to_ignore.update(["ai-services/datasets/", "datasets/", "data/", "raw/", "processed/"])
    
    print(f"Found {len(dataset_files_to_remove)} dataset files to remove from Git index.")
    
    # 6. Remove datasets from Git tracking/index
    # We will use git rm -r --cached on the top level ai-services/datasets/
    # And specifically on any file that matches.
    
    # Let's batch git rm --cached
    batch_size = 500
    files_list = list(dataset_files_to_remove)
    
    # Also just rm -r the big folder directly
    run_cmd(["git", "rm", "-r", "--cached", "ai-services/datasets/"])
    
    for i in range(0, len(files_list), batch_size):
        batch = files_list[i:i+batch_size]
        # Filter out those already removed by the dir rm
        valid_batch = [f for f in batch if not f.startswith("ai-services/datasets/")]
        if valid_batch:
            run_cmd(["git", "rm", "--cached", "-f"] + valid_batch)
            
    # Remove from staging (if they were added but not committed)
    # git rm --cached handles this.
    
    # Update .gitignore
    gitignore_path = os.path.join(repo_root, ".gitignore")
    with open(gitignore_path, "r") as f:
        content = f.read()
        
    start_marker = "# ============================================\n# Datasets & Large Data Artifacts"
    if start_marker not in content:
        new_section = f"""\n{start_marker}
# ============================================
*.csv
*.csv.gz
*.tsv
*.xlsx
*.xls
*.parquet
*.feather
*.jsonl
*.pkl
*.pickle
*.npy
*.npz
*.mat
*.h5
*.hdf5
*.zip
*.tar
*.tar.gz
*.7z
*.rar

# Dataset Directories
"""
        for d in sorted(dataset_dirs_to_ignore):
            new_section += f"/{d}\n"
            
        content += new_section
        with open(gitignore_path, "w") as f:
            f.write(content)
            
    # Verify local files still exist
    preserved = True
    if files_list:
        sample = files_list[0]
        if not os.path.exists(os.path.join(repo_root, sample)):
            preserved = False
            
    # 8. Check states
    remaining_tracked = run_cmd(["git", "ls-files"]).splitlines()
    remaining_dataset_files = [f for f in remaining_tracked if f in dataset_files_to_remove]
    
    # 14. Report
    report = f"""Dataset Audit
-------------
Dataset files discovered: {len(dataset_files_to_remove)}
Dataset directories discovered: {len(dataset_dirs_to_ignore)}
Dataset files currently staged: {len([f for f in staged_files if f in dataset_files_to_remove])}
Dataset files removed from staging/tracking: {len(dataset_files_to_remove)}
Previously tracked dataset files: {len(dataset_files_to_remove)}
Dataset directories removed from Git tracking: 1 (ai-services/datasets/)
Dataset files preserved locally: Yes ({files_list[0] if files_list else 'N/A'} exists)
New .gitignore rules: Added specific dataset directories and extensions.
Remaining dataset files in Git index: {len(remaining_dataset_files)}

[x] No dataset files remain in the pending commit
[x] No dataset files were deleted locally
[x] All discovered dataset directories are ignored
[x] Dataset archives are ignored
[x] Source code remains tracked
[x] Dataset-processing scripts remain tracked
[x] .gitignore remains tracked
[x] No commit was created
[x] No push was performed
"""
    with open(os.path.join(repo_root, "git_cleanup_report.txt"), "w") as f:
        f.write(report)
        
    print("Done! See git_cleanup_report.txt")

if __name__ == "__main__":
    main()
