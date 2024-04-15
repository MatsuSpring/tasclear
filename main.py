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
conn.commit()
conn.close()

nowTime = int(time.time())


class Task(ft.Row):
    def __init__(self, properties, lsitInstance):
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
                expand=1,
            ),
            ft.IconButton(
                ft.icons.EDIT_OUTLINED,
                tooltip='Edit Task',
                on_click=lambda e: print('Edit clicked')
            ),
            ft.IconButton(
                ft.icons.DELETE_OUTLINED,
                tooltip='Dlete Task',
                on_click=lambda e: print('Delete clicked')
            )
        ]
        self.lsitInstance = lsitInstance
    
    def onCompletedChenged(self, e):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute('UPDATE tasks SET completed=? WHERE id=?', (e.control.value, self.taskId))
        co.commit()
        co.close()
        self.lsitInstance.sortByCompletedAndDeadline()
        
    
    def onTaskTaped(self, e):
        self.dlgTaskDetails = ft.AlertDialog(
            title=ft.Text(value=self.taskName),
            content=ft.Text(value='提出期限  {}'.format(self.taskDeadlineText))
        )
        self.page.dialog = self.dlgTaskDetails
        self.dlgTaskDetails.open = True
        self.page.update()


class TaskList(ft.Column):
    def __init__(self):
        super().__init__()
        print('TaskList __init__')
        self.getFromDatabase()
    
    def sortByCompletedAndDeadline(self):
        self.controls = []
        self.getFromDatabase()
        self.update()
    
    def getFromDatabase(self):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute('SELECT * FROM tasks ORDER BY completed, deadline')
        for p in cu.fetchall():
            print(p)
            self.controls.append(Task(p, self))
         

class TaskField(ft.Column):
    def __init__(self):
        super().__init__()
        self.tl = TaskList()
        self.controls=[
            self.tl,
            ft.Row(controls=[ft.ElevatedButton(
                text='Add Task',
                expand=1,
                on_click=lambda e: print('Add clicked')
            )])
        ]
        
    def build(self):
        pass



def main(page: ft.Page):
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

    tf = TaskField()

    page.add(tf)
    
ft.app(main)
