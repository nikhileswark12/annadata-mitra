import os
import json
import hashlib
import glob
from collections import defaultdict
from PIL import Image

def get_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def verify_image(file_path):
    try:
        if os.path.getsize(file_path) == 0:
            return False, "zero_byte"
        with Image.open(file_path) as img:
            img.verify()
        return True, "ok"
    except Exception as e:
        return False, "corrupted"

def main():
    base_dir = r"f:\WP\Annadata Mitra\annadata-mitra\ai-services\datasets\vision\canonical"
    
    splits = ["train", "validation", "test"]
    physical_stats = {}
    class_sets = {}
    
    total_physical_count = 0
    all_hashes = defaultdict(list)
    corrupted_files = []
    zero_byte_files = []
    
    for split in splits:
        split_dir = os.path.join(base_dir, split)
        physical_stats[split] = defaultdict(int)
        class_sets[split] = set()
        
        if os.path.exists(split_dir):
            for cls in os.listdir(split_dir):
                cls_dir = os.path.join(split_dir, cls)
                if os.path.isdir(cls_dir):
                    class_sets[split].add(cls)
                    files = glob.glob(os.path.join(cls_dir, "*.*"))
                    physical_stats[split][cls] = len(files)
                    total_physical_count += len(files)
                    
                    for f in files:
                        is_valid, reason = verify_image(f)
                        if not is_valid:
                            if reason == "zero_byte":
                                zero_byte_files.append(f)
                            else:
                                corrupted_files.append(f)
                        else:
                            file_hash = get_hash(f)
                            all_hashes[file_hash].append((split, f))
    
    print("--- PHYSICAL COUNTS ---")
    print(f"Total Images: {total_physical_count}")
    for split in splits:
        count = sum(physical_stats[split].values())
        print(f"{split.capitalize()}: {count} images, {len(class_sets[split])} classes")
    
    print("\n--- CLASS CONSISTENCY ---")
    train_classes = class_sets.get("train", set())
    val_classes = class_sets.get("validation", set())
    test_classes = class_sets.get("test", set())
    
    print(f"Train Classes: {len(train_classes)}")
    print(f"Validation Classes: {len(val_classes)}")
    print(f"Test Classes: {len(test_classes)}")
    
    missing_in_val = train_classes - val_classes
    missing_in_test = train_classes - test_classes
    print(f"Missing in Validation: {missing_in_val}")
    print(f"Missing in Test: {missing_in_test}")
    
    print("\n--- DATASET INTEGRITY ---")
    print(f"Zero Byte Files: {len(zero_byte_files)}")
    print(f"Corrupted Files: {len(corrupted_files)}")
    
    duplicate_hashes = 0
    cross_split_leakage = 0
    
    for h, file_list in all_hashes.items():
        if len(file_list) > 1:
            duplicate_hashes += len(file_list) - 1
            splits_present = set([s for s, f in file_list])
            if len(splits_present) > 1:
                cross_split_leakage += 1
                
    print(f"Duplicate Files: {duplicate_hashes}")
    print(f"Cross-Split Leakages (distinct hashes across splits): {cross_split_leakage}")
    
    print("\n--- METADATA COMPARISON ---")
    meta_files = ["dataset_manifest.json", "preprocessing_report.json", "class_statistics.json", "classes.json", "label_mapping.json"]
    for m in meta_files:
        path = os.path.join(base_dir, m)
        if os.path.exists(path):
            print(f"Found {m}")
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        print(f"Keys: {list(data.keys())[:10]}")
                        if "total_images" in data:
                            print(f"  total_images: {data['total_images']}")
                        if "total_classes" in data:
                            print(f"  total_classes: {data['total_classes']}")
                        if "class_count" in data:
                            print(f"  class_count: {data['class_count']}")
                        if "total_files" in data:
                            print(f"  total_files: {data['total_files']}")
                    elif isinstance(data, list):
                        print(f"List length: {len(data)}")
                except Exception as e:
                    print(f"Error reading {m}: {e}")
        else:
            print(f"Missing {m}")
            
    print("\n--- STRATIFICATION (TRAIN) ---")
    for cls in sorted(physical_stats["train"].keys()):
        print(f"{cls}: {physical_stats['train'][cls]}")

if __name__ == "__main__":
    main()
