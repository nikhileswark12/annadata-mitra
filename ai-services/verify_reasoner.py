from reasoning.vision_reasoner import VisionReasoner
from core.knowledge_loader import knowledge_loader
from services.vision_service import RealVisionPredictor

print("--- Test VisionReasoner directly ---")
knowledge = knowledge_loader.load('vision', 'disease_knowledge') or {}
r = VisionReasoner.reason([0.1, 0.9, 0.0], ['a', 'early_blight', 'c'])
c = VisionReasoner.calculate_confidence(r)
e = VisionReasoner.generate_explanation(r, c, knowledge)
print("Reason:", r)
print("Confidence:", c)
print("Explanation:", e)

print("\n--- Test unknown disease ---")
r_unk = VisionReasoner.reason([0.1, 0.9, 0.0], ['a', 'alien_disease', 'c'])
c_unk = VisionReasoner.calculate_confidence(r_unk)
e_unk = VisionReasoner.generate_explanation(r_unk, c_unk, knowledge)
print("Explanation (Unknown):", e_unk)

print("\n--- Test Vision Predictor Format ---")
pred = RealVisionPredictor()
resp = pred.format_response(r, c, e)
print("Response (Known):", resp)
resp_unk = pred.format_response(r_unk, c_unk, e_unk)
print("Response (Unknown):", resp_unk)
