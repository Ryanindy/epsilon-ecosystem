import requests
import json

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5NTRhM2RhMS1mNjczLTQyODQtYjY3Zi1mNmVlMjAyM2MzMmMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU2NjI1MDI1fQ.4XXobU5XSH6jLa12A_s_SJnfp_2QxJ8esAfwxZ2B2sM"
BASE_URL = "http://localhost:5678/api/v1"
HEADERS = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

CHAT_ID = 7468069393

def send_test():
    wf_data = {
        "name": "Temp Test Telegram",
        "nodes": [
            {
                "parameters": {},
                "id": "start-node",
                "name": "When clicking "Execute Workflow"",
                "type": "n8n-nodes-base.manualTrigger",
                "typeVersion": 1,
                "position": [100, 300]
            },
            {
                "parameters": {
                    "chatId": str(CHAT_ID),
                    "text": "🔱 *Epsilon Prime Test Message*

Your Telegram workflow is now up and operational.

Status: NOMINAL",
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
            "When clicking "Execute Workflow"": {
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
        }
    }

    print("Creating temporary test workflow...")
    resp = requests.post(f"{BASE_URL}/workflows", headers=HEADERS, json=wf_data)
    if resp.status_code != 200:
        print(f"Failed to create workflow: {resp.text}")
        return
    
    wf_id = resp.json()['data']['id']
    print(f"Workflow created with ID: {wf_id}")

    print("Executing workflow...")
    # Manual execution via API is tricky, but we can try to activate and trigger if it had a trigger
    # Or use the executions endpoint if possible.
    # Actually, we can just use the 'test' execution if we had a browser, but here we use the API.
    # We can use a Webhook instead of manualTrigger.
    
    # Let's just use the existing workflow but trigger it with a simple webhook if I can find one.
    # Or I can just delete this temp one and use another approach.
    
    # Wait, I can just use the 'n8n execute' CLI if available.
    
    # Let's try to update the existing workflow to add a simple Webhook trigger that doesn't need a secret.
    pass

if __name__ == "__main__":
    send_test()
