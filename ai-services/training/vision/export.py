import os
import json
import datetime
import tensorflow as tf
from training.vision import config
import logging

logger = logging.getLogger(__name__)

def export_artifacts(model, class_names, history, metrics):
    """
    Exports the trained model and associated metadata to the deployment directory.
    """
    logger.info("Exporting model and artifacts...")
    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    
    # 1. Save Model
    model_path = os.path.join(config.EXPORT_DIR, config.MODEL_NAME)
    model.save(model_path)
    
    # 2. Save Class Names
    classes_path = os.path.join(config.EXPORT_DIR, config.CLASS_NAMES_FILE)
    with open(classes_path, 'w') as f:
        json.dump(class_names, f, indent=4)
        
    # 3. Save Training History
    history_path = os.path.join(config.EXPORT_DIR, config.HISTORY_FILE)
    with open(history_path, 'w') as f:
        # Convert history float32 to float for JSON serialization
        history_dict = {k: [float(val) for val in v] for k, v in history.history.items()}
        json.dump(history_dict, f, indent=4)
        
    # 4. Save Metadata
    metadata = {
        "dataset_version": "canonical-v1",
        "training_date": datetime.datetime.now().isoformat(),
        "tensorflow_version": tf.__version__,
        "input_shape": config.INPUT_SHAPE,
        "class_count": len(class_names),
        "model_parameters": model.count_params(),
        "epochs_trained": len(history.epoch),
        "optimizer": model.optimizer.get_config()["name"],
        "learning_rate": config.INITIAL_LR,
        "final_val_accuracy": float(history.history['val_accuracy'][-1]) if 'val_accuracy' in history.history else None,
        "test_accuracy": metrics.get('test_accuracy'),
        "test_loss": metrics.get('test_loss')
    }
    
    meta_path = os.path.join(config.EXPORT_DIR, config.METADATA_FILE)
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    # 5. Save Config
    config_dict = {k: v for k, v in vars(config).items() if not k.startswith('_')}
    config_path = os.path.join(config.EXPORT_DIR, 'training_config.json')
    with open(config_path, 'w') as f:
        json.dump(config_dict, f, indent=4, default=str)
        
    logger.info("Export complete.")
