import os
import logging
from training.vision import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_dataset_integrity():
    """Verifies that the canonical dataset structure is complete and healthy."""
    logger.info("Verifying dataset integrity...")
    
    splits = [config.TRAIN_DIR, config.VAL_DIR, config.TEST_DIR]
    class_sets = []
    
    for split_dir in splits:
        if not os.path.exists(split_dir):
            raise FileNotFoundError(f"Missing dataset split directory: {split_dir}")
            
        classes = [d for d in os.listdir(split_dir) if os.path.isdir(os.path.join(split_dir, d))]
        if not classes:
            raise ValueError(f"No classes found in {split_dir}")
            
        class_sets.append(set(classes))
        
        # Check for empty folders
        for c in classes:
            c_path = os.path.join(split_dir, c)
            files = [f for f in os.listdir(c_path) if os.path.isfile(os.path.join(c_path, f))]
            if not files:
                raise ValueError(f"Empty class directory detected: {c_path}")
                
    # Ensure all splits have the exact same classes
    if not (class_sets[0] == class_sets[1] == class_sets[2]):
        raise ValueError("Mismatch in class categories across train/val/test splits.")
        
    logger.info(f"Dataset integrity verified. Found {len(class_sets[0])} classes.")
    return sorted(list(class_sets[0]))

def ensure_export_dir():
    """Ensures export directory exists."""
    os.makedirs(config.EXPORT_DIR, exist_ok=True)
