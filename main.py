import flet as ft
import sqlite3
import time
import datetime

AppName = 'MyToDo(仮)'
DatabaseName = 'main.db'

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

nowTime = datetime.datetime.now()
nowTimeSecond = int(time.time())

class setTime(ft.Column):
    def __init__(self, t):
        super().__init__()
        self.dpYear = ft.Dropdown(
            width=207,
            options=[ft.dropdown.Option(i) for i in range(t.year, t.year+3)],
            value=t.year,
            text_size=18,
            content_padding=15,
            alignment=ft.alignment.center
        )
        self.dpMonth = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(1, 13)],
            value=t.month,
            text_size=18,
            content_padding=10,
            alignment=ft.alignment.center
        )
        self.dpDay = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(1, 32)],
            value=t.day,
            text_size=18,
            content_padding=10,
            alignment=ft.alignment.center
        )
        self.dpHour = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(0, 24)],
            value=t.hour,
            text_size=18,
            content_padding=10,
            alignment=ft.alignment.center
        )
        self.dpMin = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(0, 60)],
            value=t.minute,
            text_size=18,
            content_padding=10,
            alignment=ft.alignment.center
        )
    
        self.controls=[
            ft.Text('提出期限', size=18),
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


class Task(ft.Row):
    def __init__(self, properties, lsitInstance):
        super().__init__()
        self.taskId = properties[0]
        self.taskLessonId = properties[1]
        self.taskName = properties[2]
        self.taskDeadlineSecond = properties[3]
        self.taskDeadline = datetime.datetime.fromtimestamp(self.taskDeadlineSecond)
        self.taskDeadlineText = '{:0=4}/{:0=2}/{:0=2} {:0=2}:{:0=2}'.format(
            self.taskDeadline.year,
            self.taskDeadline.month,
            self.taskDeadline.day,
            self.taskDeadline.hour,
            self.taskDeadline.minute
        )
        self.taskCompleted = bool(properties[4])

        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute('SELECT lesson_name FROM lessons WHERE id=?',(self.taskLessonId,))
        self.taskLessonName = cu.fetchone()[0]
        print(self.taskLessonName)
        co.commit()
        co.close()

        if self.taskCompleted:
            self.taskTextStyle = ft.TextStyle(
                size=23,
                color=ft.colors.GREY,
                decoration=ft.TextDecoration.LINE_THROUGH
            )
        elif self.taskDeadlineSecond-nowTimeSecond<86400:
            self.taskTextStyle = ft.TextStyle(
                size=23,
                color=ft.colors.RED_600
            )
        else:
            self.taskTextStyle = ft.TextStyle(size=23)
        

        self.controls=[
            ft.Checkbox(value=self.taskCompleted, on_change=self.onCompletedChenged),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        text=self.taskName+'\n',
                        style=self.taskTextStyle,
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
                on_click=self.editTaskClicked
            ),
            ft.IconButton(
                ft.icons.DELETE_OUTLINED,
                tooltip='Dlete Task',
                on_click=self.deleteTaskClicked
            )
        ]
        self.lsitInstance = lsitInstance
    
    def onCompletedChenged(self, e):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute('UPDATE tasks SET completed=? WHERE id=?', (e.control.value, self.taskId))
        co.commit()
        co.close()
        self.lsitInstance.rebuild()
        
    def onTaskTaped(self, e):
        self.dlgTaskDetails = ft.AlertDialog(
            title=ft.Text(value=self.taskName),
            content=ft.Column(controls=[
                ft.Text(value='科目 : '+self.taskLessonName, size=20),
                ft.Text(value='提出期限  {}'.format(self.taskDeadlineText))
            ],
            tight=True)

        )
        self.page.dialog = self.dlgTaskDetails
        self.dlgTaskDetails.open = True
        self.page.update()
    
    def editTaskClicked(self, e):
        self.taskNameField = ft.TextField(
            label='タスク名',
            value=self.taskName,
            text_size=20,
            content_padding=15
        )
        self.setDeadline = setTime(self.taskDeadline)
        self.bsEditTask = ft.BottomSheet(
            dismissible=True,
            enable_drag=True,
            show_drag_handle=True,
            use_safe_area=True,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text('タスクを編集', size=30),
                        self.taskNameField,
                        self.setDeadline,
                        ft.Row(controls=[
                            ft.ElevatedButton(text='キャンセル', on_click=self.closeBs), 
                            ft.FilledButton(text='変更', on_click=self.editTaskDatabase),
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
        self.page.overlay.append(self.bsEditTask)
        self.page.update()
    
    def closeBs(self, e):
        self.bsEditTask.open = False
        self.bsEditTask.update()
    
    def editTaskDatabase(self, e):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute("UPDATE tasks SET task_name=?,deadline=?,completed=? WHERE id=?",(self.taskNameField.value,self.setDeadline.timeToSec(),self.taskCompleted,self.taskId))
        co.commit()
        co.close()
        self.lsitInstance.rebuild()
        self.closeBs(e)

    def deleteTaskClicked(self, e):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute('DELETE FROM tasks WHERE id=?', (self.taskId,))
        co.commit()
        co.close()
        self.lsitInstance.rebuild()


class TaskList(ft.Column):
    def __init__(self, lesson_id):
        super().__init__()
        self.lesson_id = lesson_id

    def build(self):
        self.controls=[]
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute('SELECT * FROM tasks WHERE lesson_id=? ORDER BY completed, deadline', (self.lesson_id,))
        for p in cu.fetchall():
            print(p)
            self.controls.append(Task(p, self))
        co.close()

    def rebuild(self):
        self.build()
        self.update()
    
    

class TaskField(ft.Column):
    def __init__(self, lesson_id, tabsInstance):
        super().__init__()
        self.lesson_id = lesson_id
        self.tl = TaskList(self.lesson_id)
        self.controls=[
            ft.Container(height=15),
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
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE_ROUNDED,
                        tooltip='Delete Lesson',
                        on_click=self.confirmDeleteLesson
                    )
                ]
            ),
            self.tl,
        ]
        self.scroll=ft.ScrollMode.AUTO

        self.tabsInstance = tabsInstance

    def addTask(self, e):
        self.taskNameField = ft.TextField(
            label='タスク名',
            text_size=20,
            content_padding=15
        )
        self.setDeadline = setTime(nowTime)
        self.bsAddTask = ft.BottomSheet(
            dismissible=True,
            enable_drag=True,
            show_drag_handle=True,
            use_safe_area=True,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text('タスクを追加', size=30),
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
        self.bsAddTask.update()
    
    def addTaskToDatabase(self, e):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute("INSERT INTO tasks (lesson_id,task_name,deadline,completed) VALUES(?,?,?,?)",(self.lesson_id,self.taskNameField.value,self.setDeadline.timeToSec(),False))
        co.commit()
        co.close()
        self.tl.rebuild()
        self.closeBs(e)
    
    def confirmDeleteLesson(self, e):
        self.dlgConfirmDeleteLesson = ft.AlertDialog(
            title=ft.Text('確認'),
            content=ft.Text('この授業を削除します。よろしいですか？'),
            actions=[
                ft.ElevatedButton(text='キャンセル', on_click=self.closeDlg), 
                ft.FilledButton(text='OK', on_click=self.deleteLesson),
            ],
        )
        self.page.dialog = self.dlgConfirmDeleteLesson
        self.dlgConfirmDeleteLesson.open=True
        self.page.update()

    def deleteLesson(self, e):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute("DELETE FROM lessons WHERE id=?",(self.lesson_id,))
        cu.execute("DELETE FROM tasks WHERE lesson_id=?",(self.lesson_id,))
        co.commit()
        co.close()
        self.page.dialog.open = False
        self.page.update()
        self.tabsInstance.rebuild()
    
    def closeDlg(self, e):
        self.page.dialog.open = False
        self.page.update()


class taskFieldTabs(ft.Tabs):
    def __init__(self):
        super().__init__()
        self.selected_index=0
        self.animation_duration=300
        self.scrollable=True
        self.expand=1
    
    def build(self):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute("SELECT * FROM lessons ORDER BY id ASC")
        self.lessons = cu.fetchall()
        co.commit()
        co.close()

        self.tabs = []
        for lesson in self.lessons:
            self.tabs.append(
                ft.Tab(
                    text=lesson[1],
                    content=TaskField(lesson[0], self)
                )
            )

        if len(self.tabs)==0:
            contentAddButton = ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.ADD),
                    ft.Text('授業を追加')
                ]),
                on_click=self.addLesson
            )
        else:
            contentAddButton = ft.IconButton(
                icon=ft.icons.ADD,
                on_click=self.addLesson
            )

        self.tabs.append(
            ft.Tab(
                tab_content=contentAddButton
                )
            )
            
    
    def rebuild(self):
        self.build()
        self.update()
    
    def addLesson(self, e):
        self.LessonNameField = ft.TextField(
            label='授業名',
            text_size=20,
            content_padding=15
        )
        self.bsAddLesson = ft.BottomSheet(
            dismissible=True,
            enable_drag=True,
            show_drag_handle=True,
            use_safe_area=True,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text('授業を追加', size=30),
                        self.LessonNameField,
                        ft.Row(controls=[
                            ft.ElevatedButton(text='キャンセル', on_click=self.closeBs), 
                            ft.FilledButton(text='追加', on_click=self.addLessonToDatabase),
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
        self.page.overlay.append(self.bsAddLesson)
        self.page.update()
    
    def closeBs(self, e):
        self.bsAddLesson.open = False
        self.bsAddLesson.update()
    
    def addLessonToDatabase(self, e):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        cu.execute("INSERT INTO lessons (lesson_name) VALUES(?)",(self.LessonNameField.value,))
        co.commit()
        co.close()
        self.build()
        # 追加した授業のタブを選択
        self.selected_index=len(self.tabs)-2
        self.update()
        self.closeBs(e)




def main(page: ft.Page):
    page.title = AppName
    page.theme_mode = 'light'
    theme = ft.Theme(
        color_scheme_seed=ft.colors.GREEN_400
    )
    page.theme = theme
    page.dark_theme = theme
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE_ROUNDED),
        leading_width=70,
        title=ft.Text(AppName),
        center_title=True,
        bgcolor=theme.color_scheme_seed
    )

    tft = taskFieldTabs()

    page.add(tft)

    
ft.app(main)
