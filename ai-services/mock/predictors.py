from interfaces.prediction_interface import PredictionInterface
from core.knowledge_loader import knowledge_loader

class MockCropPredictor(PredictionInterface):
    def load_model(self):
        pass

    def load_knowledge(self, processed_data):
        return knowledge_loader.load('crop', 'mock_recommendations')

    def reason(self, processed_data, knowledge):
        return knowledge

class MockVisionPredictor(PredictionInterface):
    def load_model(self):
        pass

    def preprocess(self, input_data):
        input_data.seek(0)
        file_bytes = input_data.read()[:500]
        hash_val = sum(file_bytes) % 10
        return hash_val

    def load_knowledge(self, processed_data):
        return knowledge_loader.load('vision', 'mock_diseases')

    def reason(self, processed_data, knowledge):
        diseases = knowledge
        disease = diseases[processed_data]
        return disease

    def format_response(self, reasoning, confidence, explanation):
        knowledge = knowledge_loader.load('vision', 'disease_knowledge') or {}
        k = knowledge.get(reasoning, {})
        return {
            "disease": reasoning,
            "confidence": 87,
            "severity": k.get("severity", "Unknown"),
            "description": k.get("description", f"Mock model predicted {reasoning} based on leaf symptoms."),
            "treatment": k.get("treatment", "1. Remove affected leaves.\n2. Apply appropriate fungicide if necessary.")
        }

class MockMarketPredictor(PredictionInterface):
    def load_model(self):
        pass

    def load_knowledge(self, processed_data):
        return knowledge_loader.load('market', 'mock_data')

    def reason(self, processed_data, knowledge):
        return knowledge
