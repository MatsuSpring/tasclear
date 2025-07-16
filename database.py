import sqlite3

DatabaseName = 'main.db'

def init_db():
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS lessons(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson_name STRING
            )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson_id INTEGER KEY,
                task_name STRING,
                deadline INTEGER,
                completed BOOL
            )''')
    conn.commit()
    conn.close()

def get_lesson_name(lesson_id):
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()
    cur.execute('SELECT lesson_name FROM lessons WHERE id=?', (lesson_id,))
    lesson_name = cur.fetchone()[0]
    conn.close()
    return lesson_name

def get_tasks_by_lesson(lesson_id):
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()
    tasks = cur.execute('SELECT * FROM tasks WHERE lesson_id=? ORDER BY completed, deadline', (lesson_id,)).fetchall()
    conn.close()
    return tasks

def get_all_lessons():
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()
    lessons = cur.execute("SELECT * FROM lessons ORDER BY id ASC").fetchall()
    conn.close()
    return lessons

def add_lesson(lesson_name):
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()
    cur.execute("INSERT INTO lessons (lesson_name) VALUES(?)", (lesson_name,))
    conn.commit()
    conn.close()

def add_task(lesson_id, task_name, deadline):
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (lesson_id,task_name,deadline,completed) VALUES(?,?,?,?)", (lesson_id, task_name, deadline, False))
    conn.commit()
    conn.close()

def update_task_completion(task_id, completed):
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()
    cur.execute('UPDATE tasks SET completed=? WHERE id=?', (completed, task_id))
    conn.commit()
    conn.close()

def update_task(task_id, task_name, deadline, completed):
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET task_name=?,deadline=?,completed=? WHERE id=?", (task_name, deadline, completed, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    conn.commit()
    conn.close()

def delete_lesson(lesson_id):
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()
    cur.execute("DELETE FROM lessons WHERE id=?", (lesson_id,))
    cur.execute("DELETE FROM tasks WHERE lesson_id=?", (lesson_id,))
    conn.commit()
    conn.close()
