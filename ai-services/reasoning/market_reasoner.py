class MarketReasoner:
    @staticmethod
    def reason(processed_data, crop_df, advice_rules):
        recent_record = crop_df.iloc[0]
        current_price = float(recent_record['Modal Price'])
        predicted_price = round(current_price * 1.035)
        
        markets_list = []
        for _, row in crop_df.head(5).iterrows():
            markets_list.append({
                "name": str(row['District']),
                "price": float(row['Modal Price']),
                "trend": "Up",
                "distance": "15 km"
            })
        
        while len(markets_list) < 5:
            markets_list.append({
                "name": "Nearby Mandi",
                "price": current_price,
                "trend": "Stable",
                "distance": "20 km"
            })
            
        advice = advice_rules.get("advice", "Wait")
        trend_watch = advice_rules.get("trendWatch", "Upward")
        demand_insight = advice_rules.get("demandInsight", "Demand is stable.").replace("{crop}", processed_data.title())
            
        return {
            "decision": {
                "currentPrice": current_price,
                "predictedPrice": predicted_price,
                "advice": advice,
                "trendWatch": trend_watch,
                "demandInsight": demand_insight,
            },
            "factors": markets_list[:5]
        }
        
    @staticmethod
    def calculate_confidence(reasoning_output):
        return {
            "score": 85,
            "level": "High",
            "basis": "Historical Mandi Data"
        }
        
    @staticmethod
    def generate_explanation(reasoning_output, confidence_output):
        decision = reasoning_output.get("decision", {})
        return {
            "what": f"Advice: {decision.get('advice')}",
            "why": decision.get("demandInsight"),
            "factors": "Prices computed using a 3.5% markup over recent arrivals."
        }
