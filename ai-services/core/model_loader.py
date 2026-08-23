import os
import joblib

class ModelLoader:
    @staticmethod
    def load_sklearn_model(model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        return joblib.load(model_path)

    @staticmethod
    def load_tflite_model(model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"TFLite model not found at {model_path}")
        # import tflite_runtime.interpreter as tflite
        # return tflite.Interpreter(model_path=model_path)
        pass
