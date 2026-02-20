import sqlite3
import json
db_path = 'C:/Users/Media Server/.n8n/database.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT executionId, data FROM execution_data WHERE executionId = 87")
row = cursor.fetchone()
if row:
    data = json.loads(row[1])
    # The structure is flattened in newer n8n versions or it's an array of strings representing indexes
    # Let's just print the whole thing to a file to inspect
    with open('execution_87_full.json', 'w') as f:
        json.dump(data, f, indent=2)
conn.close()
