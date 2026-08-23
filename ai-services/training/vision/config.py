import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASET_DIR = os.path.join(BASE_DIR, 'datasets', 'vision', 'canonical')
EXPORT_DIR = os.path.join(BASE_DIR, 'models', 'vision')

# Dataset splits
TRAIN_DIR = os.path.join(DATASET_DIR, 'train')
VAL_DIR = os.path.join(DATASET_DIR, 'val')
TEST_DIR = os.path.join(DATASET_DIR, 'test')

# Model parameters
IMAGE_SIZE = (224, 224)
INPUT_SHAPE = (224, 224, 3)
BATCH_SIZE = 8
CNN_FILTERS = [32, 64, 128, 256]
DROPOUT_RATE = 0.5

# Training hyperparameters
EPOCHS = 30
INITIAL_LR = 1e-3
MIN_LR = 1e-6
PATIENCE_EARLY_STOP = 5
PATIENCE_REDUCE_LR = 2

# Output files
MODEL_NAME = 'vision_model.keras'
CLASS_NAMES_FILE = 'class_names.json'
METADATA_FILE = 'model_metadata.json'
HISTORY_FILE = 'training_history.json'
METRICS_FILE = 'evaluation_metrics.json'
CONFUSION_MATRIX_FILE = 'confusion_matrix.csv'
