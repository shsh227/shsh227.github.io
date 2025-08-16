import sqlite3

conn = sqlite3.connect('goodnews.db')
cursor = conn.cursor()
for row in cursor.execute('SELECT * FROM news'):
    print(row)
conn.close()
