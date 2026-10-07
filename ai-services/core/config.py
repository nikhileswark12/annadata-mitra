import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT = int(os.environ.get("PORT", 7000))
    ENV = os.environ.get("FLASK_ENV", "development")
    # Paths
    MODEL_DIR = os.path.join(os.path.dirname(__file__), '../../models')
    DATASET_DIR = os.path.join(os.path.dirname(__file__), '../../datasets')
    
    CROP_MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/crop_model.pkl')
    CROP_SCALER_PATH = os.path.join(os.path.dirname(__file__), '../models/crop_scaler.pkl')
    
    VISION_MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/vision_model.h5')
    VISION_CLASS_NAMES_PATH = os.path.join(os.path.dirname(__file__), '../models/class_names.json')
    
    MANDI_CSV_PATH = os.path.join(os.path.dirname(__file__), '../datasets/mandi/mandi_prices.csv')

    # Explicitly opt into synthetic/mock predictors for local development only.
    # Production deployments must keep this disabled.
    USE_MOCK_MODELS = os.environ.get("USE_MOCK_MODELS", "false").strip().lower() == "true"
