import sqlite3
db_path = 'C:/Users/Media Server/.n8n/database.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for t in tables:
    print(t[0])
conn.close()
