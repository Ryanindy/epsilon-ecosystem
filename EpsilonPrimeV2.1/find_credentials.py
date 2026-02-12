import sqlite3
import os

db_path = os.path.expanduser('~/.n8n/database.sqlite')
if not os.path.exists(db_path):
    print(f"Error: {db_path} not found.")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type FROM credentials_entity WHERE type = 'telegramApi'")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Type: {row[2]}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
