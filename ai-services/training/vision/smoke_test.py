import os
import tensorflow as tf
from training.vision import config
from training.vision.model_builder import build_model
from training.vision.dataset_loader import load_datasets
from training.vision.evaluate import evaluate_model
from training.vision.export import export_artifacts

def run_smoke_test():
    print("=== VISION PIPELINE SMOKE TEST ===")
    
    # Use smoke test directory for all exports to avoid overwriting production artifacts
    config.EXPORT_DIR = os.path.join(config.BASE_DIR, 'models', 'vision', 'smoke_test')
    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    
    # Check GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"GPU Available: {len(gpus)} GPU(s) found.")
    else:
        print("GPU Not Available: Running on CPU.")
    
    # 1. Load Data
    print("\n--- 1. Loading Datasets ---")
    train_ds, val_ds, test_ds, class_names = load_datasets()
    num_classes = len(class_names)
    print(f"Discovered {num_classes} canonical classes.")
    
    # Grab one batch to verify shapes
    for images, labels in train_ds.take(1):
        print("Batch Image Shape:", images.shape)
        print("Batch Label Shape:", labels.shape)
        break
        
    # 2. Build Architecture
    print("\n--- 2. Building Architecture ---")
    model = build_model(num_classes)
    print(f"Model parameters: {model.count_params()}")
    
    # 3. Forward Pass & Backward Pass (Mini Training)
    print("\n--- 3. Training Smoke Test (1 Epoch / 2 Steps) ---")
    
    # We take only 2 batches for the smoke test
    smoke_train_ds = train_ds.take(2)
    smoke_val_ds = val_ds.take(1)
    
    history = model.fit(
        smoke_train_ds,
        validation_data=smoke_val_ds,
        epochs=1,
        verbose=1
    )
    print("Smoke Training Complete. Loss:", history.history['loss'][0])
    
    # 4. Save and Reload Model
    print("\n--- 4. Model Serialization Test ---")
    smoke_model_path = os.path.join(config.EXPORT_DIR, 'vision_model_smoke_test.keras')
    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    
    model.save(smoke_model_path)
    print(f"Model saved to {smoke_model_path}")
    
    reloaded_model = tf.keras.models.load_model(smoke_model_path)
    print("Model reloaded successfully.")
    
    # Verify predictions after reload
    for images, labels in smoke_val_ds.take(1):
        preds = reloaded_model.predict(images, verbose=0)
        print("Reloaded Model Prediction Shape:", preds.shape)
        break
        
    # 5. Full Export Pipeline Verification
    print("\n--- 5. Export Pipeline Verification ---")
    metrics, cm_df = evaluate_model(reloaded_model, smoke_val_ds, class_names)
    export_artifacts(reloaded_model, class_names, history, metrics)
    print("All artifacts exported successfully.")
    
    print("\n=== SMOKE TEST PASSED ===")

if __name__ == "__main__":
    run_smoke_test()
