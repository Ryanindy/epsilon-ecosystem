import json
import os

webhook_dir = r"I:\ARSENAL\Webhooks"
results = []

print(f"[*] Starting n8n Integrity Scan in {webhook_dir}...")

for file in os.listdir(webhook_dir):
    if file.endswith('.json'):
        path = os.path.join(webhook_dir, file)
        status = "OK"
        details = ""
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Check for n8n specific keys (some might be raw nodes, some full workflows)
                if isinstance(data, list):
                    details = f"List of {len(data)} nodes"
                elif isinstance(data, dict):
                    if 'nodes' in data:
                        details = f"Full Workflow ({len(data['nodes'])} nodes)"
                    else:
                        details = f"Dict with keys: {list(data.keys())[:3]}"
                else:
                    status = "WARNING"
                    details = f"Unknown type: {type(data).__name__}"
                    
        except Exception as e:
            status = "ERROR"
            details = str(e)
            
        results.append((file, status, details))

print("\nINTEGRITY REPORT:")
print(f"{'FILE':<45} | {'STATUS':<10} | {'DETAILS'}")
print("-" * 80)
for f, s, d in results:
    print(f"{f:<45} | {s:<10} | {d}")