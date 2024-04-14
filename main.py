import flet as ft
import sqlite3
import time
import datetime

AppName = 'MyToDo(仮)'
DatabaseName = 'main.db'

conn = sqlite3.connect(DatabaseName)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name STRING,
            deadline INTEGER,
            completed BOOL
        )''')
cur.execute('INSERT INTO tasks(task_name,deadline,completed) VALUES("英作文",1713157200,1)')
conn.commit()
conn.close()

nowTime = int(time.time())

class taskField(ft.Row):
    def __init__(self, properties):
        super().__init__()
        self.taskId = properties[0]
        self.taskName = properties[1]
        self.taskDeadlineSecond = properties[2]
        self.taskDeadline = datetime.datetime.fromtimestamp(self.taskDeadlineSecond)
        self.taskDeadlineText = '{:0=4}/{:0=2}/{:0=2} {:0=2}:{:0=2}'.format(
                self.taskDeadline.year,
                self.taskDeadline.month,
                self.taskDeadline.day,
                self.taskDeadline.hour,
                self.taskDeadline.minute
        )
        self.taskCompleted = bool(properties[3])

        self.controls=[
            ft.Checkbox(value=self.taskCompleted, on_change=self.onCompletedChenged),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        text=self.taskName+'\n',
                        style=ft.TextStyle(
                            size=23,
                            color=ft.colors.RED_600 if self.taskDeadlineSecond-nowTime<86400 else None
                        ),
                        on_click=self.onTaskTaped,
                    ),
                    ft.TextSpan(
                        text=self.taskDeadlineText,
                        style=ft.TextStyle(color=ft.colors.GREY),
                        on_click=self.onTaskTaped,
                    ),
                ],
                no_wrap=True,
            ),
        ]
    
    def onCompletedChenged(self, e):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute('UPDATE tasks SET completed={} WHERE id={}'.format(e.control.value, self.taskId))
        co.commit()
        co.close()
    
    def onTaskTaped(self, e):
        self.dlgTaskDetails = ft.AlertDialog(
            title=ft.Text(value=self.taskName),
            content=ft.Text(value='提出期限  {}'.format(self.taskDeadlineText))
        )
        self.page.dialog = self.dlgTaskDetails
        self.dlgTaskDetails.open = True
        self.page.update()
        

def main(page: ft.Page):
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()

    def closeDatabase(e):
        conn.close()

    page.title = AppName
    page.theme_mode = 'light'
    theme = ft.Theme(
        color_scheme_seed=ft.colors.GREEN_500
    )
    page.theme = theme
    page.dark_theme = theme
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.FACT_CHECK_ROUNDED),
        leading_width=40,
        title=ft.Text(AppName),
        center_title=True,
        bgcolor=theme.color_scheme_seed
    )
    

    cur.execute('SELECT * FROM tasks WHERE id=1')
    row=cur.fetchall()
    print(row[0])
    
    tf = taskField(row[0])
    page.on_disconnect=closeDatabase
    page.add(tf)
    
ft.app(main)
