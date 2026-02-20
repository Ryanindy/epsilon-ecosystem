import sqlite3
import json
db_path = 'C:/Users/Media Server/.n8n/database.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT executionId, data FROM execution_data ORDER BY executionId DESC LIMIT 5")
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}")
    # data is usually a large JSON string
    try:
        data = json.loads(row[1])
        print(json.dumps(data, indent=2)[:1000] + "...")
    except:
        print(row[1][:1000] + "...")
    print("-" * 50)
conn.close()
