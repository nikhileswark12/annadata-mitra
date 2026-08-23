import logging
from abc import ABC, abstractmethod

class PredictionInterface(ABC):
    def initialize(self):
        """Loads models and configs"""
        self._initialized = False
        self._model_loaded = False
        self._fallback_active = False
        
        try:
            self.load_model()
            self._model_loaded = True
            self._initialized = True
        except Exception as e:
            logging.error(f"Failed to load model for {self.__class__.__name__}: {e}")
            self._fallback_active = True
            self._initialized = True # Initialized with fallback

    def health(self):
        return {
            "service": self.__class__.__name__,
            "initialized": getattr(self, '_initialized', False),
            "model_loaded": getattr(self, '_model_loaded', False),
            "fallback_active": getattr(self, '_fallback_active', False),
            "version": "1.0",
            "ready": getattr(self, '_initialized', False)
        }

    def metadata(self):
        return {
            "service_name": self.__class__.__name__,
            "version": "1.0"
        }
        
    def reload(self):
        self.initialize()

    @abstractmethod
    def load_model(self):
        pass

    def predict(self, input_data):
        try:
            self.validate(input_data)
            processed = self.preprocess(input_data)
            knowledge = self.load_knowledge(processed)
            reasoning = self.reason(processed, knowledge)
            confidence = self.calculate_confidence(reasoning)
            explanation = self.generate_explanation(reasoning, confidence)
            return self.format_response(reasoning, confidence, explanation)
        except Exception as e:
            logging.error(f"Prediction pipeline error in {self.__class__.__name__}: {e}")
            raise e

    # Pipeline Stages (Overridable)
    def validate(self, input_data):
        pass

    def preprocess(self, input_data):
        return input_data

    def load_knowledge(self, processed_data):
        return None

    def reason(self, processed_data, knowledge):
        return processed_data

    def calculate_confidence(self, reasoning):
        return 100

    def generate_explanation(self, reasoning, confidence):
        return ""

    def format_response(self, reasoning, confidence, explanation):
        return reasoning
