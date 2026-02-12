import sqlite3
import os

db_path = os.path.expanduser('~/.n8n/database.sqlite')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- TABLES ---")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
for row in cursor.fetchall():
    print(row[0])

print("\n--- ACTIVE WEBHOOKS ---")
try:
    cursor.execute("SELECT * FROM webhook_entity")
    for row in cursor.fetchall():
        print(row)
except Exception as e:
    print(f"Error: {e}")

conn.close()