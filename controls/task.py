import flet as ft
import datetime
import storage as db
from controls.set_time import setTime

nowTime = datetime.datetime.now()
nowTimeSecond = int(nowTime.timestamp())

class Task(ft.Row):
    def __init__(self, page: ft.Page, properties, lsitInstance):
        super().__init__()
        self.page = page
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

        self.taskLessonName = db.get_lesson_name(self.page, self.taskLessonId)

        if self.taskCompleted:
            self.taskTextStyle = ft.TextStyle(
                size=23,
                color=ft.Colors.GREY,
                decoration=ft.TextDecoration.LINE_THROUGH
            )
        elif self.taskDeadlineSecond-nowTimeSecond<86400:
            self.taskTextStyle = ft.TextStyle(
                size=23,
                color=ft.Colors.RED_600
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
                        style=ft.TextStyle(color=ft.Colors.GREY),
                        on_click=self.onTaskTaped,
                    ),
                ],
                expand=1,
            ),
            ft.IconButton(
                ft.Icons.EDIT_OUTLINED,
                tooltip='Edit Task',
                on_click=self.editTaskClicked
            ),
            ft.IconButton(
                ft.Icons.DELETE_OUTLINED,
                tooltip='Dlete Task',
                on_click=self.deleteTaskClicked
            )
        ]
        self.lsitInstance = lsitInstance
    
    def onCompletedChenged(self, e):
        db.update_task_completion(self.page, self.taskId, e.control.value)
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
        db.update_task(self.page, self.taskId, self.taskNameField.value, self.setDeadline.timeToSec(), self.taskCompleted)
        self.lsitInstance.rebuild()
        self.closeBs(e)

    def deleteTaskClicked(self, e):
        db.delete_task(self.page, self.taskId)
        self.lsitInstance.rebuild()