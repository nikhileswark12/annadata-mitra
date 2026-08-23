import requests

def test_weather():
    print("Testing /weather-risk endpoint...")
    payload = {"location": "Delhi", "crop": "Wheat"}
    res = requests.post("http://localhost:7000/weather-risk", json=payload)
    print("Status Code:", res.status_code)
    try:
        print("Response:", res.json())
    except:
        print("Response Text:", res.text)

    print("\nTesting /health endpoint...")
    res_health = requests.get("http://localhost:7000/health")
    print("Status Code:", res_health.status_code)
    try:
        print("Response:", res_health.json())
    except:
        print("Response Text:", res_health.text)

if __name__ == "__main__":
    test_weather()
