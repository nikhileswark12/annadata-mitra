class CropReasoner:
    @staticmethod
    def reason_ml(probs, classes, knowledge):
        sorted_indices = probs.argsort()[::-1][:3]
        
        decisions = []
        factors = []
        for idx in sorted_indices:
            crop_name = classes[idx]
            confidence = int(probs[idx] * 100)
            ranges = knowledge.get(crop_name, {})
            icon = ranges.get('icon', '🌱')
            
            decisions.append({
                "crop": crop_name,
                "confidence": confidence,
                "icon": icon,
                "season": ranges.get('season', []),
                "sowing": ranges.get('sowing', ''),
                "harvest": ranges.get('harvest', '')
            })
            
        while len(decisions) < 3:
            decisions.append({"crop": "Unknown", "confidence": 0, "icon": ""})
            
        return {
            "decision": decisions,
            "factors": factors
        }
        
    @staticmethod
    def reason_rules(inp, crop_knowledge, params):
        param_keys = params.get('PARAM_KEYS', [])
        param_labels = params.get('PARAM_LABELS', {})
        param_units = params.get('PARAM_UNITS', {})
        
        scores = []
        for crop_name, ranges in crop_knowledge.items():
            matched, mismatched = [], []
            for key in param_keys:
                val = inp.get(key, 0)
                if key in ranges:
                    lo, hi = ranges[key]
                    label = param_labels.get(key, key)
                    unit  = param_units.get(key, '')
                    if lo <= val <= hi:
                        matched.append(f"{label} ({val}{unit} ✓)")
                    else:
                        mismatched.append(f"{label} {val}{unit} outside ideal {lo}–{hi}{unit}")
                        
            score = round(len(matched) / max(1, len(param_keys)) * 100)
            if score < 40:
                continue
                
            matched_str = ', '.join(matched[:3]) if matched else 'none'
            reasoning = f"Your {matched_str} match {crop_name.title()} requirements."
            if mismatched:
                reasoning += f" Note: {mismatched[0]}."
                
            scores.append({
                'crop':       crop_name,
                'confidence': score,
                'reasoning':  reasoning,
                'icon':       ranges.get('icon', '🌱'),
                'season':     ', '.join(ranges.get('season', [])),
                'sowing':     ranges.get('sowing', ''),
                'harvest':    ranges.get('harvest', ''),
            })

        scores.sort(key=lambda x: x['confidence'], reverse=True)
        top3 = scores[:3]

        if len(top3) == 0:
            top3 = [{
                'crop': 'chickpea', 'confidence': 35,
                'reasoning': 'No crop strongly matched your inputs. Chickpea is drought-tolerant and may still be viable. Please consult your local KVK.',
                'icon': '🫘', 'season': 'Rabi', 'sowing': 'October–November', 'harvest': 'February–March'
            }] * 3
            
        while len(top3) < 3:
            top3.append(top3[-1])

        return {
            "decision": top3,
            "factors": []
        }

    @staticmethod
    def calculate_confidence(reasoning_output, is_ml=True):
        decisions = reasoning_output.get("decision", [])
        top_score = decisions[0].get("confidence", 0) if decisions else 0
        level = "High" if top_score > 75 else "Medium" if top_score > 50 else "Low"
        return {
            "score": top_score,
            "level": level,
            "basis": "ML Probability" if is_ml else "Rule Match"
        }
        
    @staticmethod
    def generate_explanation(reasoning_output, confidence_output, is_ml=True):
        decisions = reasoning_output.get("decision", [])
        top_crop = decisions[0]["crop"] if decisions else "Unknown"
        
        if is_ml:
            what = f"Recommended crops starting with {top_crop.title()}."
            why = f"Based on ML model prediction ({confidence_output['score']}% match)."
            factors = "Soil and climate inputs matched against trained RandomForest patterns."
        else:
            what = f"Recommended crops starting with {top_crop.title()}."
            why = decisions[0].get("reasoning", "Rule-based ICAR agronomic engine.")
            factors = "ICAR thresholds and optimal ranges."
            
        return {
            "what": what,
            "why": why,
            "factors": factors
        }
