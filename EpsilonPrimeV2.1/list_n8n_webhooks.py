import sqlite3
db_path = 'C:/Users/Media Server/.n8n/database.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM webhook_entity")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
