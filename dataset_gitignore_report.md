# Dataset Gitignore Audit Report

## 1. `.gitignore` Changes Made
A new, clearly separated section for **Datasets & Large Data Artifacts** has been appended/updated in the `.gitignore`.
It covers file patterns (`.csv`, `.xlsx`, `.zip`, `.parquet`, `.tar.gz`, etc.) and directory patterns (`datasets/`, `data/`, `raw/`, etc.).

## 2. Dataset Directories Identified
The following specific dataset directories were physically located and dynamically added to `.gitignore`:
- `ai-services/datasets/`
- `ai-services/datasets/crop/raw/`
- `ai-services/datasets/vision/PlantVillage/`

## 3. Already-Tracked Datasets (Action Required)
Since `.gitignore` does not remove files that are already tracked by Git, you must manually run `git rm --cached <file>` on the following files before committing:
- `ai-services/datasets/crop/raw/Crop_recommendation.csv`
- `ai-services/datasets/crop/reports/crop_class_distribution.csv`
- `ai-services/datasets/crop/splits/test.csv`
- `ai-services/datasets/crop/splits/train.csv`
- `ai-services/datasets/crop/splits/val.csv`
- `ai-services/datasets/Final_Datasets_Updated/01_Market_Intelligence/AllIndia_Mandi_Prices_Multicommodity_2019.csv`
- `ai-services/datasets/Final_Datasets_Updated/01_Market_Intelligence/AllIndia_Weekly_Commodity_Prices_Aug2023.csv`
- `ai-services/datasets/Final_Datasets_Updated/01_Market_Intelligence/APMC_Monthly_Prices_Maharashtra.csv`
- `ai-services/datasets/Final_Datasets_Updated/01_Market_Intelligence/Maharashtra_APMC_Monthly_Arrivals_Prices.csv`
- `ai-services/datasets/Final_Datasets_Updated/01_Market_Intelligence/Maharashtra_MSP_CropType_2012onwards.csv`
- `ai-services/datasets/Final_Datasets_Updated/01_Market_Intelligence/Mandi_Prices_Jowar_MP.csv`
- `ai-services/datasets/Final_Datasets_Updated/01_Market_Intelligence/Mandi_Prices_Maize_MP.csv`
- `ai-services/datasets/Final_Datasets_Updated/01_Market_Intelligence/Mandi_Prices_Wheat_MP.csv`
- `ai-services/datasets/Final_Datasets_Updated/01_Market_Intelligence/MSP_Minimum_Support_Prices_Maharashtra.csv`
- `ai-services/datasets/Final_Datasets_Updated/02_Weather_Intelligence/Global_Rainfall_by_Country_Year.csv`
- `ai-services/datasets/Final_Datasets_Updated/02_Weather_Intelligence/Global_Temperature_by_Country_Year.csv`
- `ai-services/datasets/Final_Datasets_Updated/02_Weather_Intelligence/India_District_Monthly_Rainfall.csv`
- `ai-services/datasets/Final_Datasets_Updated/02_Weather_Intelligence/India_Rainfall_Subdivision_1901_2015.csv`
- `ai-services/datasets/Final_Datasets_Updated/02_Weather_Intelligence/India_State_Weather_1997_2020.csv`
- `ai-services/datasets/Final_Datasets_Updated/03_Soil_Analysis/Amritsar_Soil_Health_Card_Punjab.csv`
- `ai-services/datasets/Final_Datasets_Updated/03_Soil_Analysis/India_State_Soil_NPK_pH.csv`
- `ai-services/datasets/Final_Datasets_Updated/03_Soil_Analysis/Soil_Fertility_pH_EC_Micronutrients.csv`
- `ai-services/datasets/Final_Datasets_Updated/03_Soil_Analysis/Soil_Fertility_Prediction.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/Crop_Production_Index_Trend_2004_2012.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/FAO_Global_Crop_Yield_1961_2018.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/Foodgrains_Production_Area_Yield_2006_2011.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/Global_Crop_Yield_Weather_Pesticides.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/Global_Pesticide_Use_by_Country.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/India_Agricultural_Production_Annual_1993_2014.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/India_Crop_Prediction_StateDistrict.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/India_Crop_Production_AllStates_2010_2017.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/India_Crop_Yield_with_Soil_Weather.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/India_District_Crop_Area_Production_Yield_1997_2020.csv`
- `ai-services/datasets/Final_Datasets_Updated/04_Yield_Prediction/India_District_MultiCrop_AreaProdYield_2010_2017.csv`
- `ai-services/datasets/Final_Datasets_Updated/05_Fertilizer_Recommendation/Crop_and_Fertilizer_Maharashtra.csv`
- `ai-services/datasets/Final_Datasets_Updated/05_Fertilizer_Recommendation/Fertilizer_Advisor_SoilType_CropType.csv`
- `ai-services/datasets/Final_Datasets_Updated/05_Fertilizer_Recommendation/Fertilizer_Prediction_SoilCrop.csv`
- `ai-services/datasets/Final_Datasets_Updated/05_Fertilizer_Recommendation/Fertilizer_Prediction_TempHumidityMoisture.csv`
- `ai-services/datasets/Final_Datasets_Updated/06_Crop_Recommendation/Crop_Recommendation_NPK_Climate.csv`
- `ai-services/datasets/Final_Datasets_Updated/06_Crop_Recommendation/Crop_Variety_Recommended_Zone_India.csv`
- `ai-services/datasets/Final_Datasets_Updated/07_Irrigation_Management/Irrigation_Need_Prediction_MultiFactor_10k.csv`
- `ai-services/datasets/Final_Datasets_Updated/07_Irrigation_Management/Irrigation_Scheduling_SoilMoisture_Odisha.csv`
- `ai-services/datasets/Final_Datasets_Updated/08_Cost_of_Cultivation/Cost_of_Cultivation_Production_StateWise.csv`
- `ai-services/datasets/Final_Datasets_Updated/09_Population_Demand/India_State_Population_Census_1951_2011.csv`
- `ai-services/datasets/mandi/mandi_prices.csv`
- `ai-services/datasets/mandi/processed_prices.csv`
- `ai-services/datasets/mandi/test.csv`
- `ai-services/datasets/mandi/train.csv`
- `ai-services/datasets/mandi/val.csv`
- `ai-services/datasets/vision/Plant Disease Data/Apple__black_rot/0090d05d-d797-4c99-abd4-3b9cb323a5fd___JR_FrgE.S 8727.JPG`
- ... and 15148 more.

## 4. Files Intentionally Excluded from Ignoring
- **Source code (`.py`, `.js`, etc.):** Kept intact.
- **Config & Metadata (`.json` outside datasets, `README.md`):** Kept intact.
- **Mock/Test Data:** Small `.json` fixtures not falling under large data archives were kept.

## 5. Validation Results
`.gitignore` updated successfully.
