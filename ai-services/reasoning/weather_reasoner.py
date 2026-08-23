import logging

logger = logging.getLogger(__name__)

class WeatherReasoner:
    @staticmethod
    def reason(weather, risk_rules, no_risk_msg):
        risks = []
        for rule in risk_rules:
            try:
                condition_func = eval(rule['condition'])
                if condition_func(weather):
                    msg_func = eval(rule['message'])
                    risks.append({
                        'type':           rule['type'],
                        'severity':       rule['severity'],
                        'message':        msg_func(weather),
                        'recommendation': rule['recommendation'],
                    })
            except Exception as e:
                logger.warning(f"Risk rule '{rule.get('id')}' failed: {e}")

        if not risks:
            risks.append(no_risk_msg)

        severity_order = {'High': 0, 'Medium': 1, 'Low': 2}
        risks.sort(key=lambda r: severity_order.get(r.get('severity'), 99))
        
        return {
            "decision": risks,
            "factors": []
        }
        
    @staticmethod
    def calculate_confidence(reasoning_output):
        return {
            "score": 95,
            "level": "High",
            "basis": "Deterministic Rules"
        }
        
    @staticmethod
    def generate_explanation(reasoning_output, confidence_output):
        decisions = reasoning_output.get("decision", [])
        return {
            "what": f"Weather risks evaluated: {len(decisions)} found.",
            "why": decisions[0].get("message", "No extreme weather detected."),
            "factors": "Temperature, Humidity, Rainfall, and Wind"
        }
