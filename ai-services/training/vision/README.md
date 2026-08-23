# Vision Model Training Pipeline

This directory contains the production-grade TensorFlow/Keras training pipeline for the Annadata Mitra Vision reasoning agent.

## Architecture
- **Dataset Loading**: Native `tf.data.Dataset` mapping directly from `datasets/vision/canonical`.
- **Optimization**: Features `AUTOTUNE` prefetching, in-memory caching, and batching.
- **Augmentations**: Active during training only (RandomFlip, RandomRotation, RandomZoom, RandomContrast, RandomBrightness).
- **Model**: `MobileNetV2` (ImageNet base) + GlobalAveragePooling + BatchNormalization + Dropout(0.5) + Dense Softmax.
- **Callbacks**: EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, TensorBoard.

## Execution

**Run Dry-Run Verification:**
```bash
python train.py --dry-run
```
*(Verifies dataset integrity, loads the data pipeline, compiles the architecture, and exits before training begins)*

**Run Full Pipeline:**
```bash
python train.py
```

## Outputs
Artifacts are automatically exported to `ai-services/models/vision/`:
- `vision_model.keras`
- `class_names.json`
- `training_history.json`
- `evaluation_metrics.json`
- `model_metadata.json`
- `confusion_matrix.csv`
