import json
import os

with open('live_wf.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# The 'get' command might return the data wrapped in a 'data' key or as the root object
# Based on the previous 'get' output, it was the root object
nodes = data.get('nodes', [])
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
        print(f"Updated node: {node['name']}")

with open('live_wf_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
