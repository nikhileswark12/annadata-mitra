import argparse
import logging
import sys
import os
import tensorflow as tf

tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(2)

from training.vision import config
from training.vision.utils import verify_dataset_integrity, ensure_export_dir
from training.vision.dataset_loader import load_datasets
from training.vision.model_builder import build_model
from training.vision.trainer import train_model
from training.vision.evaluate import evaluate_model
from training.vision.export import export_artifacts

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(dry_run=False):
    logger.info("Initializing Vision Model Training Pipeline...")
    ensure_export_dir()
    
    # 1. Verification
    logger.info("Step 1: Dataset Verification")
    try:
        class_names = verify_dataset_integrity()
    except Exception as e:
        logger.error(f"Dataset verification failed: {e}")
        sys.exit(1)
        
    # 2. Loading Data
    logger.info("Step 2: Loading Data Pipelines")
    train_ds, val_ds, test_ds, ds_class_names = load_datasets()
    
    assert list(class_names) == list(ds_class_names), "Class names mismatch between utils and dataset_loader"
    num_classes = len(class_names)
    
    # 3. Build Model
    logger.info("Step 3: Building Architecture")
    model = build_model(num_classes)
    model.summary(print_fn=logger.info)
    
    if dry_run:
        logger.info("Dry-run complete. Architecture, pipelines, and datasets verified.")
        sys.exit(0)
        
    # 4. Train Model
    logger.info("Step 4: Training")
    history = train_model(model, train_ds, val_ds, epochs=config.EPOCHS)
    
    # 5. Evaluate
    logger.info("Step 5: Evaluation")
    metrics, cm_df = evaluate_model(model, test_ds, class_names)
    
    # 6. Export
    logger.info("Step 6: Exporting Artifacts")
    export_artifacts(model, class_names, history, metrics)
    
    logger.info(f"Pipeline complete! All artifacts saved to {config.EXPORT_DIR}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vision Model Training Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Initialize pipeline without training")
    args = parser.parse_args()
    
    main(dry_run=args.dry_run)
