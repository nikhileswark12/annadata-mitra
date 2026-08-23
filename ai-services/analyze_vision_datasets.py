import os
import json

def analyze_datasets(base_path):
    report = {
        "datasets": {},
        "global_stats": {
            "total_images": 0,
            "empty_folders": []
        }
    }
    
    if not os.path.exists(base_path):
        return "Base path does not exist"
        
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            dataset_name = item
            ds_info = {
                "classes": {},
                "total_images": 0,
                "splits": [],
                "annotation_format": "folder-based"
            }
            
            for root, dirs, files in os.walk(item_path):
                if not dirs and not files:
                    report["global_stats"]["empty_folders"].append(root)
                    continue
                    
                rel_path = os.path.relpath(root, item_path)
                if rel_path == ".":
                    # Check for splits
                    for d in dirs:
                        if d.lower() in ["train", "val", "test", "validation", "training", "testing"]:
                            ds_info["splits"].append(d)
                    continue
                
                parts = rel_path.split(os.sep)
                class_name = parts[-1]
                
                if files:
                    img_count = sum(1 for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')))
                    if img_count > 0:
                        if class_name not in ds_info["classes"]:
                            ds_info["classes"][class_name] = 0
                        ds_info["classes"][class_name] += img_count
                        ds_info["total_images"] += img_count
                        report["global_stats"]["total_images"] += img_count
            
            report["datasets"][dataset_name] = ds_info
            
    return json.dumps(report, indent=2)

print(analyze_datasets(r"f:\WP\Annadata Mitra\annadata-mitra\ai-services\datasets\vision"))
