import os
import json
import time
import random
import statistics
import sys
from collections import defaultdict

# Ensure we can import from ai-services
sys.path.insert(0, '.')

from services.crop_service import RealCropPredictor
from services.weather_service import RealWeatherPredictor
from services.market_service import RealMarketPredictor
from reasoning.strategist_reasoner import StrategistReasoner

def generate_e3_scenarios():
    random.seed(42)
    scenarios = []
    
    crops = ["rice", "wheat", "maize", "cotton", "sugarcane"]
    locations = ["Gujarat", "Punjab", "Maharashtra", "Karnataka", "UP"]
    
    # Generate 100 base profiles
    for i in range(100):
        c = random.choice(crops)
        loc = random.choice(locations)
        n, p, k = random.randint(20, 100), random.randint(20, 100), random.randint(20, 100)
        temp, hum = random.uniform(20.0, 35.0), random.uniform(50.0, 90.0)
        ph, rain = random.uniform(5.5, 7.5), random.uniform(50.0, 200.0)
        
        base_scenario = {
            "id": f"scen_{i}",
            "context": {"crop": c, "location": loc},
            "inputs": {
                "crop": {"nitrogen": n, "phosphorus": p, "potassium": k, "temperature": temp, "humidity": hum, "ph": ph, "rainfall": rain, "location": loc},
                "weather": {"location": loc, "crop": c},
                "market": {"crop": c, "location": loc, "quantity": 100}
            }
        }
        
        # 1. 3 Agents Available (Healthy / Conflict)
        scen_3 = json.loads(json.dumps(base_scenario))
        scen_3["id"] = f"{scen_3['id']}_3_agents"
        scen_3["type"] = "3_agents"
        scen_3["source_status"] = {"crop": "available", "weather": "available", "market": "available"}
        scen_3["upstream"] = {
            "crop": {"recommendations": [{"crop": c}]},
            "weather": {"risks": [{"risk": "Flood", "severity": "High", "advice": "Harvest immediately."}] if i % 2 == 0 else []},
            "market": {"advice": "Wait to sell." if i % 2 == 0 else "Sell now."}
        }
        scenarios.append(scen_3)
        
        # 2. 2 Agents Available (Crop Missing)
        scen_2 = json.loads(json.dumps(scen_3))
        scen_2["id"] = f"{scen_2['id']}_2_agents"
        scen_2["type"] = "2_agents"
        scen_2["source_status"]["crop"] = "failed"
        del scen_2["upstream"]["crop"]
        scenarios.append(scen_2)
        
        # 3. 1 Agent Available (Crop & Weather Missing)
        scen_1 = json.loads(json.dumps(scen_3))
        scen_1["id"] = f"{scen_1['id']}_1_agent"
        scen_1["type"] = "1_agent"
        scen_1["source_status"]["crop"] = "failed"
        scen_1["source_status"]["weather"] = "failed"
        del scen_1["upstream"]["crop"]
        del scen_1["upstream"]["weather"]
        scenarios.append(scen_1)
        
        # 4. 0 Agents Available
        scen_0 = json.loads(json.dumps(scen_3))
        scen_0["id"] = f"{scen_0['id']}_0_agents"
        scen_0["type"] = "0_agents"
        scen_0["source_status"]["crop"] = "failed"
        scen_0["source_status"]["weather"] = "failed"
        scen_0["source_status"]["market"] = "failed"
        scen_0["upstream"] = {}
        scenarios.append(scen_0)

    return scenarios

def naive_aggregation(scenario):
    actions = []
    if scenario["source_status"]["crop"] == "available":
        crop_recs = scenario["upstream"].get("crop", {}).get("recommendations", [])
        if scenario["context"]["crop"].lower() in [r.get("crop", "").lower() for r in crop_recs]:
            pass
    if scenario["source_status"]["weather"] == "available":
        risks = scenario["upstream"].get("weather", {}).get("risks", [])
        if risks:
            if "high" in risks[0].get("severity", "").lower():
                actions.append(f"Mitigate weather risk: {risks[0].get('risk', '')}")
            else:
                actions.append(f"Monitor weather: {risks[0].get('risk', '')}")
    if scenario["source_status"]["market"] == "available":
        advice = scenario["upstream"].get("market", {}).get("advice", "")
        if "wait" in advice.lower():
            actions.append("Monitor market trends for optimal selling time.")
        else:
            actions.append("Proceed with current market selling strategy.")
    return {"actions": actions}

def run_latency_experiment():
    print("Initializing components...")
    crop_predictor = RealCropPredictor()
    crop_predictor.initialize()
    weather_predictor = RealWeatherPredictor()
    weather_predictor.initialize()
    market_predictor = RealMarketPredictor()
    market_predictor.initialize()
    
    strategist_knowledge = {
        "synthesis_rules": {
            "action_ordering": {"Immediate Action": 1, "Short-term Monitoring": 2, "Informational": 3},
            "conflicts": {
                "market_wait_vs_weather_risk": {
                    "resolution": "Prioritize immediate harvest/protection over market timing due to weather threat."
                }
            },
            "uncertainty_penalties": {"missing_crop": -10, "missing_weather": -30, "missing_market": -20},
            "base_confidence": 100
        }
    }
    
    scenarios = generate_e3_scenarios()
    os.makedirs('experiments', exist_ok=True)
    with open('experiments/latency_eval_dataset.json', 'w') as f:
        json.dump(scenarios, f, indent=2)
        
    measurements = defaultdict(list)
    ITERATIONS = 10 
    
    print("Running pure-Python latency benchmark...")
    for s in scenarios:
        
        # 1. Individual Upstream Agents (only measure full info scenarios)
        if s["type"] == "3_agents":
            crop_in = s["inputs"]["crop"]
            weather_in = s["inputs"]["weather"]
            market_in = s["inputs"]["market"]
            
            for _ in range(ITERATIONS):
                t0 = time.perf_counter_ns()
                crop_predictor.predict(crop_in)
                t1 = time.perf_counter_ns()
                measurements["crop_agent"].append(t1 - t0)
                
            for _ in range(ITERATIONS):
                t0 = time.perf_counter_ns()
                weather_predictor.predict(weather_in)
                t1 = time.perf_counter_ns()
                measurements["weather_agent"].append(t1 - t0)
                
            for _ in range(ITERATIONS):
                t0 = time.perf_counter_ns()
                market_predictor.predict(market_in)
                t1 = time.perf_counter_ns()
                measurements["market_agent"].append(t1 - t0)
                
        # 2. Naive Aggregation
        for _ in range(ITERATIONS):
            t0 = time.perf_counter_ns()
            naive_aggregation(s)
            t1 = time.perf_counter_ns()
            measurements[f"naive_aggregation_{s['type']}"].append(t1 - t0)
            
        # 3. Strategist Latency
        processed_data = {
            "context": s["context"],
            "upstream": s["upstream"],
            "source_status": s["source_status"]
        }
        for _ in range(ITERATIONS):
            t0 = time.perf_counter_ns()
            reasoning_out = StrategistReasoner.reason(processed_data, strategist_knowledge)
            confidence_out = StrategistReasoner.calculate_confidence(reasoning_out)
            t1 = time.perf_counter_ns()
            measurements[f"strategist_{s['type']}"].append(t1 - t0)
            
    print("Calculating statistics...")
    results = {}
    
    for key, times_ns in measurements.items():
        times_ms = [t / 1_000_000.0 for t in times_ns] 
        results[key] = {
            "count": len(times_ms),
            "mean_ms": statistics.mean(times_ms),
            "median_ms": statistics.median(times_ms),
            "std_dev_ms": statistics.stdev(times_ms) if len(times_ms) > 1 else 0,
            "min_ms": min(times_ms),
            "max_ms": max(times_ms),
            "p95_ms": sorted(times_ms)[int(len(times_ms) * 0.95)],
            "p99_ms": sorted(times_ms)[int(len(times_ms) * 0.99)]
        }
        
    strat_mean = results["strategist_3_agents"]["mean_ms"]
    naive_mean = results["naive_aggregation_3_agents"]["mean_ms"]
    
    overhead_ms = strat_mean - naive_mean
    overhead_pct = (overhead_ms / naive_mean * 100) if naive_mean else 0
    
    results["_analysis"] = {
        "orchestration_overhead_ms": overhead_ms,
        "relative_overhead_percent": overhead_pct
    }
    
    with open('experiments/latency_experiment_results.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    print("Done. Absolute Overhead: {:.3f} ms".format(overhead_ms))

if __name__ == "__main__":
    run_latency_experiment()
