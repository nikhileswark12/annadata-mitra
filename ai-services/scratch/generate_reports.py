import json
import os

with open("scratch/dataset_analysis.json", "r") as f:
    datasets = json.load(f)

base_dir = "C:/Users/My/.gemini/antigravity-ide/brain/e971f9dd-7ec6-469e-a57b-6fdc0df0f5d6"
artifacts = ["dataset_inventory.md", "dataset_quality_report.md", "dataset_gap_analysis.md", "dataset_acquisition_plan.md", "dataset_readiness_matrix.md"]

# 1. Dataset Inventory
with open(os.path.join(base_dir, "dataset_inventory.md"), "w") as out:
    out.write("# Dataset Inventory\n\n")
    out.write("| Dataset Name | File Type | Size (MB) | Rows/Images | Columns/Classes | Target/Label Format | Missing Values | Duplicate Rows | Date Coverage | Geo Coverage | Intended Agent | Status |\n")
    out.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
    for d in datasets:
        if d['Type'] == 'Tabular':
            out.write(f"| {d['DatasetName']} | {d['FileType']} | {d['SizeMB']} | {d.get('Rows', 'N/A')} | {d.get('Columns', 'N/A')} | {d.get('Target', 'None')} | {d.get('Missing', 0)} | {d.get('Duplicates', 0)} | {d.get('DateCoverage', 'None')} | {d.get('GeoCoverage', 'None')} | {d['Agent']} | {d['Status']} |\n")
        else:
            out.write(f"| {d['DatasetName']} | {d['FileType']} | {d['SizeMB']} | {d.get('ImagesCount', 'N/A')} | {d.get('Classes', 'N/A')} | {d.get('LabelFormat', 'N/A')} | N/A | N/A | N/A | N/A | {d['Agent']} | {d['Status']} |\n")

# 2. Quality Report
with open(os.path.join(base_dir, "dataset_quality_report.md"), "w") as out:
    out.write("# Dataset Quality Report\n\n")
    out.write("| Dataset | Type | Score | Missing | Duplicates | Readiness |\n")
    out.write("| --- | --- | --- | --- | --- | --- |\n")
    for d in datasets:
        score = d.get('Score', 0)
        readiness = "Production Ready" if score >= 90 else ("Minor Cleaning Needed" if score >= 70 else ("Significant Issues" if score >= 50 else "Replace"))
        if d['Type'] == 'Tabular':
            out.write(f"| {d['DatasetName']} | Tabular | {score} | {d.get('Missing', 0)} | {d.get('Duplicates', 0)} | {readiness} |\n")
        else:
            out.write(f"| {d['DatasetName']} | Images | {score} | N/A | N/A | {readiness} |\n")

# 3. Gap Analysis
# Expected datasets: 
# Crop: Crop Recommendation Dataset, ICAR thresholds, Soil Health Card, Crop calendar
# Vision: PlantVillage, PlantDoc, IP102, DeepWeeds
# Weather: IMD Gridded Rainfall, historical weather, weather risk rules
# Market: Agmarknet historical prices, MSP datasets, mandi metadata
# Strategist: disease knowledge, crop lifecycle knowledge, government schemes, treatment database

expected = {
    "Crop Planning": ["Crop Recommendation Dataset", "ICAR thresholds", "Soil Health Card", "Crop calendar"],
    "Vision Agronomist": ["PlantVillage", "PlantDoc", "IP102", "DeepWeeds"],
    "Weather Risk": ["IMD Gridded Rainfall", "historical weather", "weather risk rules"],
    "Market Intelligence": ["Agmarknet historical prices", "MSP datasets", "mandi metadata"],
    "Strategist": ["disease knowledge", "crop lifecycle knowledge", "government schemes", "treatment database"]
}

# Simple matching
found_files = " ".join([d['DatasetName'].lower() for d in datasets])

gap_results = []
for agent, reqs in expected.items():
    for req in reqs:
        status = "Missing"
        priority = "P0 — Blocks implementation"
        
        # Simple heuristic
        if any(w in found_files for w in req.lower().split()):
            status = "Already Available"
        elif "mandi" in req.lower() and "mandi" in found_files:
            status = "Already Available"
        elif "msp" in req.lower() and "msp" in found_files:
            status = "Already Available"
        elif "agmarknet" in req.lower() and "agmarknet" in found_files:
            status = "Already Available"
        elif "soil" in req.lower() and "soil" in found_files:
            status = "Partial"
            priority = "P1 — Needed for strong performance"
        elif "weather" in req.lower() and "weather" in found_files:
            status = "Partial"
        
        if req == "PlantVillage" and "vision" in found_files: status = "Already Available"
        if req == "Crop Recommendation Dataset" and "crop_recommendation" in found_files: status = "Already Available"
        
        if status == "Missing":
            if agent in ["Vision Agronomist", "Strategist"]: priority = "P1 — Needed for strong performance"
            if req in ["PlantDoc", "IP102", "DeepWeeds"]: priority = "P2 — Improves accuracy"
            
        gap_results.append((req, status, priority, f"Core dependency for {agent}"))

with open(os.path.join(base_dir, "dataset_gap_analysis.md"), "w") as out:
    out.write("# Dataset Gap Analysis\n\n")
    out.write("| Dataset | Current Status | Priority | Why Needed |\n")
    out.write("| --- | --- | --- | --- |\n")
    for req, status, priority, why in gap_results:
        out.write(f"| {req} | {status} | {priority} | {why} |\n")

# 4. Acquisition Plan
with open(os.path.join(base_dir, "dataset_acquisition_plan.md"), "w") as out:
    out.write("# Dataset Acquisition Recommendations\n\n")
    out.write("| Missing Dataset | Official Source | Download Method | Expected Size | License | Preprocessing Needed | Target Location |\n")
    out.write("| --- | --- | --- | --- | --- | --- | --- |\n")
    for req, status, priority, why in gap_results:
        if status in ["Missing", "Partial"]:
            source = "data.gov.in / ICAR"
            if req == "PlantDoc" or req == "DeepWeeds" or req == "IP102": source = "Kaggle / Academic"
            if req == "IMD Gridded Rainfall": source = "IMD Data Portal"
            out.write(f"| {req} | {source} | API / Web Scraping | 1-10 GB | Open | Format cleaning, validation | `ai-services/datasets/{req.lower().replace(' ', '_')}` |\n")

# 5. Readiness Matrix
with open(os.path.join(base_dir, "dataset_readiness_matrix.md"), "w") as out:
    out.write("# Dataset Readiness Matrix\n\n")
    out.write("| AI Agent | Required | Found | Missing | Readiness |\n")
    out.write("| --- | --- | --- | --- | --- |\n")
    for agent, reqs in expected.items():
        found = sum(1 for req, st, pr, why in gap_results if "Available" in st and "dependency for "+agent in why)
        missing = len(reqs) - found
        readiness = f"{int((found/len(reqs))*100)}%"
        out.write(f"| {agent} | {len(reqs)} | {found} | {missing} | {readiness} |\n")

print("Generated all artifacts")