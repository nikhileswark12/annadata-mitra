class VisionReasoner:
    @staticmethod
    def reason(preds, class_names):
        import numpy as np
        max_idx = np.argmax(preds)
        confidence = float(preds[max_idx]) * 100
        disease = class_names[max_idx]
        
        return {
            "decision": {
                "disease": disease
            },
            "factors": [
                {"name": "confidence_score", "value": confidence}
            ]
        }
        
    @staticmethod
    def calculate_confidence(reasoning_output):
        factors = reasoning_output.get("factors", [])
        score = factors[0]["value"] if factors else 0
        return {
            "score": score,
            "basis": "CNN Activation Softmax"
        }
        
    @staticmethod
    def generate_explanation(reasoning_output, confidence_output, knowledge):
        decision = reasoning_output.get("decision", {})
        disease = decision.get("disease", "Unknown")
        
        # Fallback dictionary if disease is unknown
        k = knowledge.get(disease, {})
        
        severity = k.get("severity", "Unknown")
        description = k.get("description", f"AI model predicted {disease} based on leaf symptoms.")
        treatment = k.get("treatment", "1. Remove affected leaves.\n2. Ensure proper spacing for aeration.\n3. Apply appropriate fungicide if necessary.")
        recommendation = k.get("recommendation", "Monitor plants closely.")
        
        return {
            "what": f"Diagnosis: {disease}",
            "why": description,
            "factors": treatment,
            "severity": severity,
            "recommendation": recommendation
        }
