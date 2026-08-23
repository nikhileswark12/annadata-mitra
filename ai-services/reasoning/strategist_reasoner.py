class StrategistReasoner:
    @staticmethod
    def reason(processed_data, knowledge):
        context = processed_data.get("context", {})
        upstream = processed_data.get("upstream", {})
        source_status = processed_data.get("source_status", {})
        
        target_crop = context.get("crop", "Unknown")
        target_location = context.get("location", "Unknown")
        season = "Current Season"
        
        cropAdvice = ""
        marketTiming = ""
        weatherRisk = ""
        farmAdvisory = ""
        actions = []
        factors = []
        
        rules = knowledge.get("synthesis_rules", {})
        action_ordering = rules.get("action_ordering", {})
        
        # 1. Process Crop
        if source_status.get("crop") == "available":
            crop_recs = upstream.get("crop", [])
            if isinstance(crop_recs, dict) and "recommendations" in crop_recs:
                recs = crop_recs["recommendations"]
            else:
                recs = crop_recs
                
            recommended_names = [r.get("crop", "").lower() for r in recs] if isinstance(recs, list) else []
            if target_crop.lower() in recommended_names:
                cropAdvice = f"{target_crop.capitalize()} is suitable for your location based on soil and climate factors."
                factors.append("Crop suitability confirmed by Crop Agent.")
            else:
                alts = [c.capitalize() for c in recommended_names[:2]]
                alt_text = f" Consider alternatives like {', '.join(alts)}." if alts else ""
                cropAdvice = f"{target_crop.capitalize()} may not be optimal.{alt_text}"
                factors.append("Target crop not strongly recommended by Crop Agent.")
        elif source_status.get("crop") == "insufficient_input":
            cropAdvice = "Crop suitability could not be fully assessed because required soil inputs were unavailable."
            factors.append("Crop Agent lacked sufficient inputs to confirm suitability.")
        else:
            cropAdvice = "Crop suitability data unavailable."
            
        # 2. Process Weather
        has_high_weather_risk = False
        if source_status.get("weather") == "available":
            weather_data = upstream.get("weather", {})
            risks = weather_data.get("risks", [])
            if risks:
                weatherRisk = " ".join([r.get("advice", "") for r in risks])
                factors.append(f"Weather risk identified: {risks[0].get('risk', 'Unknown')}.")
                if "high" in risks[0].get("severity", "").lower():
                    has_high_weather_risk = True
                    actions.append({"text": f"Mitigate weather risk: {risks[0].get('risk', '')}", "priority": "Immediate Action"})
                else:
                    actions.append({"text": f"Monitor weather: {risks[0].get('risk', '')}", "priority": "Short-term Monitoring"})
            else:
                weatherRisk = "Favorable weather conditions expected. No immediate alerts."
                factors.append("No immediate weather risks identified by Weather Agent.")
        else:
            weatherRisk = "Weather data unavailable."
            
        # 3. Process Market
        has_market_wait = False
        market_action_text = ""
        if source_status.get("market") == "available":
            market_data = upstream.get("market", {})
            marketTiming = market_data.get("advice", "")
            if "wait" in marketTiming.lower() or "hold" in marketTiming.lower():
                has_market_wait = True
                factors.append("Market intelligence suggests holding produce.")
                market_action_text = "Monitor market trends for optimal selling time."
                actions.append({"text": market_action_text, "priority": "Short-term Monitoring"})
            else:
                factors.append("Market conditions favorable for immediate or planned sale.")
                actions.append({"text": "Proceed with current market selling strategy.", "priority": "Short-term Monitoring"})
        else:
            marketTiming = "Market intelligence unavailable."
            
        # 4. Conflict Resolution
        if has_high_weather_risk and has_market_wait:
            factors.append("Conflict detected: High weather risk vs Market wait recommendation.")
            marketTiming = rules.get("conflicts", {}).get("market_wait_vs_weather_risk", {}).get("resolution", "Prioritize immediate harvest/protection over market timing due to weather threat.")
            # Remove the conflicting market wait action
            actions = [a for a in actions if a.get("text") != market_action_text]
            actions.append({"text": "Prioritize immediate harvest or crop protection despite market timing.", "priority": "Immediate Action"})
            
        farmAdvisory = "Consult local experts for region-specific pest and disease management."
        
        # 5. Full Fallback Handling
        available_count = sum(1 for status in source_status.values() if status in ("available", "insufficient_input"))
        if available_count == 0:
            cropAdvice = "Insufficient agricultural intelligence is currently available to generate a reliable integrated plan."
            marketTiming = "Unavailable."
            weatherRisk = "Unavailable."
            farmAdvisory = "Unavailable."
            actions = [{"text": "Seek manual agricultural extension services.", "priority": "Immediate Action"}]
            
        # Deduplicate actions while preserving order based on priority
        def get_priority(action):
            return action_ordering.get(action.get("priority", "Informational"), 99)
            
        actions.sort(key=get_priority)
        
        unique_actions = []
        seen_texts = set()
        for a in actions:
            if a.get("text") not in seen_texts:
                unique_actions.append(a.get("text"))
                seen_texts.add(a.get("text"))
        
        # Ensure we have at least some action
        if not unique_actions and available_count > 0:
            unique_actions = ["Proceed with standard farming practices."]
            
        return {
            "decision": {
                "crop": target_crop,
                "location": target_location,
                "season": season,
                "cropAdvice": cropAdvice,
                "marketTiming": marketTiming,
                "weatherRisk": weatherRisk,
                "farmAdvisory": farmAdvisory,
                "actions": unique_actions
            },
            "factors": factors,
            "processed_data": processed_data,
            "knowledge": knowledge
        }
        
    @staticmethod
    def calculate_confidence(reasoning_output):
        processed_data = reasoning_output.get("processed_data", {})
        knowledge = reasoning_output.get("knowledge", {})
        source_status = processed_data.get("source_status", {})
        
        rules = knowledge.get("synthesis_rules", {})
        penalties = rules.get("uncertainty_penalties", {})
        
        base_confidence = rules.get("base_confidence", 100)
        
        available_sources = [k for k, v in source_status.items() if v == "available"]
        insufficient_sources = [k for k, v in source_status.items() if v == "insufficient_input"]
        failed_sources = [k for k, v in source_status.items() if v in ("failed", "unavailable")]
        
        if source_status.get("crop") in ("failed", "unavailable"):
            base_confidence += penalties.get("missing_crop", -10)
        elif source_status.get("crop") == "insufficient_input":
            base_confidence -= 15 # Specific penalty for missing NPK
            
        if source_status.get("weather") in ("failed", "unavailable"):
            base_confidence += penalties.get("missing_weather", -30)
            
        if source_status.get("market") in ("failed", "unavailable"):
            base_confidence += penalties.get("missing_market", -20)
            
        if not available_sources and not insufficient_sources:
            return {"score": 0, "level": "None", "basis": "No intelligence sources available."}
            
        # Penalize for conflicts
        factors = reasoning_output.get("factors", [])
        for f in factors:
            if "Conflict" in f:
                base_confidence -= 10
                
        base_confidence = max(0, min(100, base_confidence))
        
        level = "High" if base_confidence >= 80 else "Medium" if base_confidence >= 50 else "Low"
        
        active = len(available_sources) + len(insufficient_sources)
        basis = f"Based on {active} active agent(s)."
        if insufficient_sources:
            basis += f" Limited input for: {', '.join(insufficient_sources)}."
        if failed_sources:
            basis += f" Missing/Failed: {', '.join(failed_sources)}."
            
        return {"score": base_confidence, "level": level, "basis": basis}
        
    @staticmethod
    def generate_explanation(reasoning_output, confidence_output):
        processed_data = reasoning_output.get("processed_data", {})
        source_status = processed_data.get("source_status", {})
        active = sum(1 for status in source_status.values() if status in ("available", "insufficient_input"))
        
        if active == 0:
            what = "Failed to generate strategy."
            why = "All upstream agents were unavailable."
        else:
            what = f"Synthesized integrated strategy using {active} AI agent(s)."
            why = confidence_output.get("basis", "")
            
        factors = reasoning_output.get("factors", [])
        
        return {
            "what": what,
            "why": why,
            "factors": factors
        }
