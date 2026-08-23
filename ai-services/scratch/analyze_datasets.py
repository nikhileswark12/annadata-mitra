import os
import json
import pandas as pd
from collections import defaultdict
from PIL import Image

def load_data():
    with open("scratch/data_files.json", "r") as f:
        return json.load(f)

def guess_agent(path):
    p = path.lower()
    if 'crop' in p or 'soil' in p or 'fertilizer' in p: return "Crop Planning"
    if 'weather' in p or 'rainfall' in p or 'temperature' in p or 'imd' in p: return "Weather Risk"
    if 'market' in p or 'agmarknet' in p or 'price' in p or 'mandi' in p or 'msp' in p: return "Market Intelligence"
    if 'vision' in p or 'image' in p or 'leaf' in p or 'plantvillage' in p: return "Vision Agronomist"
    if 'knowledge' in p or 'scheme' in p or 'disease' in p: return "Strategist"
    return "Unknown"

def process_tabular(filepath):
    try:
        # Load a sample to avoid memory issues on huge files
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath, nrows=10000)
            # just get full row count via wc -l equivalent or assume it's small enough to load fully
            df_full = pd.read_csv(filepath)
        elif filepath.endswith('.parquet'):
            df_full = pd.read_parquet(filepath)
        elif filepath.endswith('.json'):
            df_full = pd.read_json(filepath)
        elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            df_full = pd.read_excel(filepath)
        else:
            return None
            
        rows, cols = df_full.shape
        missing = int(df_full.isnull().sum().sum())
        dupes = int(df_full.duplicated().sum())
        
        # Label/Target
        col_lower = [c.lower() for c in df_full.columns]
        target = "None"
        for t in ['label', 'target', 'class', 'disease', 'crop', 'price']:
            if t in col_lower:
                target = df_full.columns[col_lower.index(t)]
                break
                
        # Date coverage
        date_cov = "None"
        date_cols = [c for c in df_full.columns if 'date' in c.lower() or 'year' in c.lower() or 'timestamp' in c.lower()]
        if date_cols:
            try:
                min_d = df_full[date_cols[0]].min()
                max_d = df_full[date_cols[0]].max()
                date_cov = f"{min_d} to {max_d}"
            except:
                date_cov = "Present (unparseable)"
                
        # Geo coverage
        geo_cov = "None"
        geo_cols = [c for c in df_full.columns if c.lower() in ['state', 'district', 'city', 'location', 'lat', 'lon', 'latitude', 'longitude']]
        if geo_cols:
            geo_cov = f"Columns: {', '.join(geo_cols)}"
            
        # Quality score
        score = 100
        if missing > 0: score -= (missing / (rows * cols + 1)) * 100 * 2
        if dupes > 0: score -= (dupes / (rows + 1)) * 100 * 2
        score = max(0, min(100, int(score)))
        
        return {
            "Rows": rows,
            "Columns": cols,
            "Target": target,
            "Missing": missing,
            "Duplicates": dupes,
            "DateCoverage": date_cov,
            "GeoCoverage": geo_cov,
            "Score": score
        }
    except Exception as e:
        return {"Error": str(e)}

def run_analysis():
    files = load_data()
    base_dir = "f:/Annadata Mitra/annadata-mitra"
    
    # Group images by directory
    image_exts = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
    tabular_exts = {".csv", ".xlsx", ".xls", ".json", ".parquet"}
    
    image_dirs = defaultdict(list)
    tabular_files = []
    other_files = []
    
    for f in files:
        if f['ext'] in image_exts:
            dirname = os.path.dirname(f['path'])
            image_dirs[dirname].append(f)
        elif f['ext'] in tabular_exts:
            tabular_files.append(f)
        else:
            other_files.append(f)
            
    results = []
    
    # Process tabular
    print(f"Processing {len(tabular_files)} tabular files...")
    for tf in tabular_files:
        full_path = os.path.join(base_dir, tf['path'])
        stats = process_tabular(full_path)
        if stats and "Error" not in stats:
            res = {
                "DatasetName": os.path.basename(tf['path']),
                "FilePath": tf['path'],
                "FileType": tf['ext'],
                "SizeMB": round(tf['size'] / (1024*1024), 2),
                "Agent": guess_agent(tf['path']),
                "Type": "Tabular"
            }
            res.update(stats)
            res["Status"] = "Complete" if res["Score"] >= 70 else "Partial"
            results.append(res)
            
    # Process images by top-level dataset dir
    # Aggregate subdirectories into a main dataset if possible
    # For simplicity, let's group by the top 3 levels of directory
    grouped_img_datasets = defaultdict(list)
    for d, flist in image_dirs.items():
        parts = d.split(os.sep)
        # Assuming datasets/vision/canonical/... 
        # Group by first 3 levels (e.g. datasets/vision/canonical)
        group_key = os.sep.join(parts[:3]) if len(parts) >= 3 else d
        grouped_img_datasets[group_key].extend(flist)
        
    print(f"Processing {len(grouped_img_datasets)} image datasets...")
    for gkey, flist in grouped_img_datasets.items():
        classes = set([os.path.basename(os.path.dirname(f['path'])) for f in flist])
        total_size = sum([f['size'] for f in flist])
        
        # Sample one image for resolution
        sample_res = "Unknown"
        try:
            if flist:
                with Image.open(os.path.join(base_dir, flist[0]['path'])) as img:
                    sample_res = f"{img.width}x{img.height}"
        except:
            pass
            
        res = {
            "DatasetName": os.path.basename(gkey) + " (Images)",
            "FilePath": gkey,
            "FileType": "Images",
            "SizeMB": round(total_size / (1024*1024), 2),
            "Agent": guess_agent(gkey),
            "Type": "Images",
            "ImagesCount": len(flist),
            "Classes": len(classes),
            "Resolution": sample_res,
            "LabelFormat": "Directory Name",
            "Score": 95, # Assuming good if present
            "Status": "Complete"
        }
        results.append(res)
        
    with open("scratch/dataset_analysis.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Done analysis.")

if __name__ == "__main__":
    run_analysis()
