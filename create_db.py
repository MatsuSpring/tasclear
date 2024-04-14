import sqlite3

dbname = 'main.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute('''CREATE TABLE tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name STRING,
                deadline INTEGER,
                completed BOOL
            )''')

conn.commit()
conn.close()