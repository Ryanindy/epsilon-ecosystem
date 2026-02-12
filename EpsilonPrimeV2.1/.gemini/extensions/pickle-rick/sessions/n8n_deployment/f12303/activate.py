import requests

url = "http://localhost:5678/api/v1/workflows/iTQxhWots2Y2x3k6"
headers = {
    "X-N8N-API-KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5NTRhM2RhMS1mNjczLTQyODQtYjY3Zi1mNmVlMjAyM2MzMmMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU2NjI1MDI1fQ.4XXobU5XSH6jLa12A_s_SJnfp_2QxJ8esAfwxZ2B2sM",
    "Content-Type": "application/json"
}
data = {"active": True}

response = requests.patch(url, headers=headers, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
