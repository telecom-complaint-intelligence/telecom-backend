import httpx
import json

url = "http://localhost:8001/api/v1/analyze"
payload = {"complaint": "Tower is not burning!!!"}

try:
    with httpx.Client(timeout=10.0) as client:
        response = client.post(url, json=payload)
        print("Status Code:", response.status_code)
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error querying AI service:", e)
