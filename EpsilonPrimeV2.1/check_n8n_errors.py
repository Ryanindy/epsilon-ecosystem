import sqlite3
import os
import json

db_path = os.path.expanduser('~/.n8n/database.sqlite')
if not os.path.exists(db_path):
    db_path = 'C:/Users/Media Server/.n8n/database.sqlite'

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Join execution_entity and execution_data to get error details
# In n8n v1+, errors are stored in execution_data.data (JSON)
query = """
SELECT 
    e.id, 
    e.status, 
    e.stoppedAt, 
    d.data as executionData
FROM execution_entity e
LEFT JOIN execution_data d ON e.id = d.executionId
WHERE e.workflowId = 'lVPaseLISPQwuY44'
ORDER BY e.stoppedAt DESC
LIMIT 5
"""

try:
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print(f"--- RECENT EXECUTIONS FOR WORKFLOW lVPaseLISPQwuY44 ---")
    
    for row in rows:
        print(f"ID: {row['id']} | Status: {row['status']} | Time: {row['stoppedAt']}")
        
        if row['executionData']:
            try:
                data = json.loads(row['executionData'])
                # n8n execution data is a list of objects/arrays
                # Look for 'error' key in the objects
                found_error = False
                for item in data:
                    if isinstance(item, dict) and 'error' in item:
                        error_info = item['error']
                        print(f"Error Type: {error_info.get('name', 'Unknown')}")
                        print(f"Message: {error_info.get('message', 'No message')}")
                        if 'stack' in error_info:
                            print(f"Stack: {error_info['stack'][:300]}...")
                        found_error = True
                        break
                if not found_error:
                    # Sometimes error is elsewhere in the structure
                    print("Could not find specific error object in executionData JSON.")
            except Exception as e:
                print(f"Could not parse executionData: {e}")
        else:
            print("No executionData found for this ID.")
        print("-" * 60)

except sqlite3.OperationalError as e:
    print(f"Database Error: {e}")

conn.close()
