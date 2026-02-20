import requests
import json

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5NTRhM2RhMS1mNjczLTQyODQtYjY3Zi1mNmVlMjAyM2MzMmMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU2NjI1MDI1fQ.4XXobU5XSH6jLa12A_s_SJnfp_2QxJ8esAfwxZ2B2sM"
BASE_URL = "http://localhost:5678/api/v1"
HEADERS = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

WF_ID = "lVPaseLISPQwuY44"

def fix():
    # 1. Get
    print(f"Fetching workflow {WF_ID}...")
    resp = requests.get(f"{BASE_URL}/workflows/{WF_ID}", headers=HEADERS)
    resp.raise_for_status()
    full_data = resp.json()

    # 2. Extract editable fields - nodes, connections, name, settings are likely the set
    editable_fields = ['name', 'nodes', 'connections', 'settings']
    wf_obj = {k: full_data[k] for k in editable_fields if k in full_data}
    
    # 3. Modify
    nodes = wf_obj.get('nodes', [])
    for node in nodes:
        if node['name'] == 'Ask Epsilon Prime':
            node['parameters']['options'] = {
                'headerParametersUI': {
                    'parameter': [
                        {
                            'name': 'Authorization',
                            'value': 'Bearer epsilon-dev-key'
                        }
                    ]
                }
            }
            print(f"Injected Auth header into node: {node['name']}")

    # 4. Update
    print("Updating workflow...")
    resp = requests.put(f"{BASE_URL}/workflows/{WF_ID}", headers=HEADERS, json=wf_obj)
    if resp.status_code != 200:
        print(f"Update failed: {resp.status_code} - {resp.text}")
    else:
        print("Workflow updated successfully.")

    # 5. Activate
    requests.post(f"{BASE_URL}/workflows/{WF_ID}/activate", headers=HEADERS)

if __name__ == "__main__":
    fix()
