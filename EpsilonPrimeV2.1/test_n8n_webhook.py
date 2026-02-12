import requests
import json

url = "https://mediaserver.taild49f5e.ts.net/webhook/telegram-uplink"
headers = {"Content-Type": "application/json"}
payload = {
  "update_id": 1000,
  "message": {
    "message_id": 1,
    "from": { "id": 1, "is_bot": False, "first_name": "TestUser" },
    "chat": { "id": 12345, "type": "private" },
    "date": 1620000000,
    "text": "Hello from Pickle Rick"
  }
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")