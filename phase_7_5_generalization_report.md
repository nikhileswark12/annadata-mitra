# Phase 7.5 Generalization Report

## 1. Objective
The objective of Phase 7.5 is to rigorously evaluate the generalization performance of the frozen models (Crop Random Forest and Vision MobileNetV2) on the canonical test datasets, confirming that they maintain performance and reproducing the results from Phase 6.8 and Phase 6.11 respectively.

## 2. Research Freeze Compliance
- **Crop model and dataset**: Untouched.
- **Vision model weights and dataset**: Untouched.
- **Rules (Weather, Market, Strategist)**: Untouched.
- **E1 - E4 Artifacts**: Untouched.
- **API Contracts & Codebase**: Untouched.
- **Modifications**: ONLY the `run_e5_generalization_experiment.py` script was patched.

## 3. Forensic Findings Summary
The previous run of the E5 evaluation reported a catastrophic failure for the Vision model (1.48% accuracy). A forensic audit confirmed this was **not a genuine model failure** but an **invalid evaluation pipeline**:
1. **Model Mismatch**: Loaded the untrained baseline model instead of the trained `vision_model_improved.keras`.
2. **Preprocessing Mismatch**: Scaled pixels to `[0, 1]` instead of MobileNetV2's required `[-1, 1]` via `preprocess_input`.
3. **Keras 3 Deserialization**: The script failed to map Keras 2 layers (TFOpLambda, functional engine, BatchNormalization axis list) properly when loading in Keras 3.

## 4. Fixes Applied
The following patches were applied to `run_e5_generalization_experiment.py`:
- Updated the model path to `models/vision/improved/vision_model_improved.keras`.
- Swapped `rescale=1./255` for `mobilenet_v2.preprocess_input`.
- Injected a robust recursive deserialization patch to strip broken layers and dynamically fix compatibility parameters before loading.
- Retained `shuffle=False`, `steps=len(test_generator)`, and seed `42`.

## 5. Experimental Design
- **Crop Model**: Evaluated on `datasets/crop/splits/test.csv`, scaling features using the scaler fitted on `train.csv`.
- **Vision Model**: Evaluated on `datasets/vision/canonical/test`, predicting batches sequentially.
- **Metrics**: Accuracy, Precision, Recall, F1 (Macro & Weighted), Confusion Matrix, Inference Time.

## 6. Crop Generalization Results
*Results pending execution completion...*

## 7. Vision Generalization Results
*Results pending execution completion...*

## 8. Runtime Analysis
*Results pending execution completion...*

## 9. Reproducibility Comparison
*Results pending execution completion...*

## 10. Statistical Summary
*Results pending execution completion...*

## 11. Limitations
*Results pending execution completion...*

## 12. Research Claims Supported
*Results pending execution completion...*

## 13. Final Classification
*Results pending execution completion...*
