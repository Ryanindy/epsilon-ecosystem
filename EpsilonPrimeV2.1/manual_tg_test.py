import requests
import json
import time

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5NTRhM2RhMS1mNjczLTQyODQtYjY3Zi1mNmVlMjAyM2MzMmMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU2NjI1MDI1fQ.4XXobU5XSH6jLa12A_s_SJnfp_2QxJ8esAfwxZ2B2sM"
BASE_URL = "http://localhost:5678/api/v1"
HEADERS = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

CHAT_ID = 7468069393

def run():
    wf_data = {
        "name": "Manual Test Telegram Message",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "test-tg-msg",
                    "options": {}
                },
                "id": "webhook-node",
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [100, 300],
                "webhookId": "test-tg-msg"
            },
            {
                "parameters": {
                    "chatId": str(CHAT_ID),
                    "text": "EPSILON PRIME SYSTEM CHECK\n\nTelegram Workflow: UP\nBridge Connectivity: NOMINAL\n\n_This is an automated test message._",
                    "additionalFields": {
                        "parse_mode": "Markdown"
                    }
                },
                "id": "telegram-node",
                "name": "Telegram",
                "type": "n8n-nodes-base.telegram",
                "typeVersion": 1,
                "position": [300, 300],
                "credentials": {
                    "telegramApi": {
                        "id": "QdDdSN8YnT9Ap8mx"
                    }
                }
            }
        ],
        "connections": {
            "Webhook": {
                "main": [
                    [
                        {
                            "node": "Telegram",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "settings": {
            "saveExecutionProgress": True,
            "saveManualExecutions": True
        }
    }

    print("Creating workflow...")
    resp = requests.post(f"{BASE_URL}/workflows", headers=HEADERS, json=wf_data)
    print(f"Response Status: {resp.status_code}")
    print(f"Response Body: {resp.text}")
    if resp.status_code != 200:
        return
    
    wf_id = resp.json()['id'] # Try without ['data']
    print(f"Workflow created with ID: {wf_id}")

    print("Activating workflow...")
    requests.post(f"{BASE_URL}/workflows/{wf_id}/activate", headers=HEADERS)

    # Give it a second to register the webhook
    time.sleep(2)

    print("Triggering test message...")
    url = "http://localhost:5678/webhook/test-tg-msg"
    resp = requests.post(url, json={})
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")

    # Clean up
    print("Deleting temporary workflow...")
    requests.delete(f"{BASE_URL}/workflows/{wf_id}", headers=HEADERS)

if __name__ == "__main__":
    run()
