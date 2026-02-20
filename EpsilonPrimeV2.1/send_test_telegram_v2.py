import requests
import json

url = "http://localhost:5678/webhook/91421f33-f72f-4d83-813a-4cac42780d22/webhook"
payload = {
  "update_id": 713821124,
  "message": {
    "message_id": 15,
    "from": {
      "id": 7468069393,
      "is_bot": False,
      "first_name": "Ryan",
      "username": "Ryanindy83"
    },
    "chat": {
      "id": 7468069393,
      "type": "private"
    },
    "date": 1771316572,
    "text": "TEST: Send me a message from Epsilon Prime."
  }
}

print(f"Sending mock Telegram message to {url}...")
try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
