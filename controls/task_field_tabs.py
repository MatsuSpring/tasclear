import flet as ft
import database as db
from controls.task_field import TaskField

class taskFieldTabs(ft.Tabs):
    def __init__(self):
        super().__init__()
        self.selected_index=0
        self.animation_duration=300
        self.scrollable=True
        self.expand=1
    
    def build(self):
        self.lessons = db.get_all_lessons()

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
                    ft.Icon(ft.Icons.ADD),
                    ft.Text('授業を追加')
                ]),
                on_click=self.addLesson
            )
        else:
            contentAddButton = ft.IconButton(
                icon=ft.Icons.ADD,
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
        db.add_lesson(self.LessonNameField.value)
        self.build()
        # 追加した授業のタブを選択
        self.selected_index=len(self.tabs)-2
        self.update()
        self.closeBs(e)
