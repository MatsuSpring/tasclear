import flet as ft
import datetime
import storage as db
from controls.task_list import TaskList
from controls.set_time import setTime

nowTime = datetime.datetime.now()

class TaskField(ft.Column):
    def __init__(self, page: ft.Page, lesson_id, tabsInstance):
        super().__init__()
        self.page = page
        self.lesson_id = lesson_id
        self.tl = TaskList(self.page, self.lesson_id)
        self.controls=[
            ft.Container(height=15),
            ft.Row(
                controls=[
                    ft.FilledTonalButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.ADD),
                                ft.Text('Add Task', size=18)
                            ],
                            height=60,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        expand=1,
                        on_click=self.addTask
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_ROUNDED,
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
        db.add_task(self.page, self.lesson_id, self.taskNameField.value, self.setDeadline.timeToSec())
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
        db.delete_lesson(self.page, self.lesson_id)
        self.page.dialog.open = False
        self.page.update()
        self.tabsInstance.rebuild()
    
    def closeDlg(self, e):
        self.page.dialog.open = False
        self.page.update()