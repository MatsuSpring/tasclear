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

nowTime = datetime.datetime.now()
nowTimeSecond = int(time.time())


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
                            color=ft.colors.RED_600 if self.taskDeadlineSecond-nowTimeSecond<86400 else None
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
        co.close()
         
class setTime(ft.Column):
    def __init__(self):
        super().__init__()
        self.dpYear = ft.Dropdown(
            width=207,
            options=[ft.dropdown.Option(i) for i in range(nowTime.year, nowTime.year+3)],
            value=nowTime.year,
            text_size=18,
            content_padding=15,
            alignment=ft.alignment.center
        )
        self.dpMonth = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(1, 13)],
            value=nowTime.month,
            text_size=18,
            content_padding=10,
            alignment=ft.alignment.center
        )
        self.dpDay = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(1, 32)],
            value=nowTime.day,
            text_size=18,
            content_padding=10,
            alignment=ft.alignment.center
        )
        self.dpHour = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(0, 24)],
            value=nowTime.hour,
            text_size=18,
            content_padding=10,
            alignment=ft.alignment.center
        )
        self.dpMin = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(0, 60)],
            value=nowTime.minute,
            text_size=18,
            content_padding=10,
            alignment=ft.alignment.center
        )
    
        self.controls=[
            ft.Row(controls=[
                self.dpYear, ft.Text('年', size=15)
            ]),
            ft.Row(controls=[
                self.dpMonth, ft.Text('月', size=15), self.dpDay, ft.Text('日', size=15)
            ]),
            ft.Row(controls=[
                self.dpHour, ft.Text('時', size=15), self.dpMin, ft.Text('分', size=15)
            ])
        ]
    
    def timeToSec(self):
        return int(datetime.datetime(year=int(self.dpYear.value), month=int(self.dpMonth.value), day=int(self.dpDay.value), hour=int(self.dpHour.value), minute=int(self.dpMin.value)).timestamp())


class TaskField(ft.Column):
    def __init__(self):
        super().__init__()
        self.tl = TaskList()
        self.controls=[
            ft.Row(
                controls=[
                    ft.FilledTonalButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.ADD),
                                ft.Text('Add Task', size=18)
                            ],
                            height=60,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        expand=1,
                        on_click=self.addTask
                    )
                ]
            ),
            self.tl,
        ]
        
    
    def addTask(self, e):
        self.taskNameField = ft.TextField(
            label='タスク名',
            text_size=20,
            content_padding=15
        )
        self.setDeadline = setTime()
        self.bsAddTask = ft.BottomSheet(
            dismissible=True,
            enable_drag=True,
            show_drag_handle=True,
            use_safe_area=True,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.taskNameField,
                        self.setDeadline,
                        ft.Row(controls=[
                            ft.ElevatedButton(text='キャンセル', on_click=self.closeBs), 
                            ft.FilledButton(text='追加', on_click=self.addTaskToDatabase),
                        ],
                        alignment=ft.MainAxisAlignment.END)
                    ],
                    alignment=ft.VerticalAlignment.CENTER,
                    tight=True,
                ),
                padding=30
            ),
            open=True,
        )
        self.page.overlay.append(self.bsAddTask)
        self.page.update()
    
    def closeBs(self, e):
        self.bsAddTask.open = False
        self.page.update()
    
    def addTaskToDatabase(self, e):
        print(self.taskNameField.value,self.setDeadline.timeToSec(),False)
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute("INSERT INTO tasks (task_name,deadline,completed) VALUES(?,?,?)",(self.taskNameField.value,self.setDeadline.timeToSec(),False))
        co.commit()
        co.close()
        self.tl.sortByCompletedAndDeadline()
        self.bsAddTask.open = False
        self.page.update()



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
    page.scroll = ft.ScrollMode.AUTO

    tf = TaskField()

    page.add(tf)
    
ft.app(main)
