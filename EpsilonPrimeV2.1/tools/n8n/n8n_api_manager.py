import requests
import json
import sys

CONFIG_PATH = ".gemini/config/api_keys.json"

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def activate_workflow(workflow_id, active=True):
    config = load_config()
    api_key = config['n8n']['api_key']
    base_url = config['n8n']['base_url']
    
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    # Try the specific activation endpoint
    url = f"{base_url}/workflows/{workflow_id}/activate"
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print(f"Success: Workflow {workflow_id} activated.")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if e.response:
            print(e.response.text)

if __name__ == "__main__":
    wf_id = sys.argv[1]
    activate_workflow(wf_id)