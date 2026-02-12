import requests
import json

wf_id = "iTQxhWots2Y2x3k6"
url = f"http://localhost:5678/api/v1/workflows/{wf_id}"
headers = {
    "X-N8N-API-KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5NTRhM2RhMS1mNjczLTQyODQtYjY3Zi1mNmVlMjAyM2MzMmMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU2NjI1MDI1fQ.4XXobU5XSH6jLa12A_s_SJnfp_2QxJ8esAfwxZ2B2sM",
    "Content-Type": "application/json"
}

# 1. Get
response = requests.get(url, headers=headers)
wf_data = response.json()

# 2. Modify
# Strip fields that might cause 400s if sent back
fields_to_keep = ['name', 'nodes', 'connections', 'settings', 'staticData', 'meta', 'pinData', 'tags']
payload = {k: v for k, v in wf_data.items() if k in fields_to_keep}
payload['active'] = True

# 3. Put
response = requests.put(url, headers=headers, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
