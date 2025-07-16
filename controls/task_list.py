import flet as ft
import storage as db
from controls.task import Task

class TaskList(ft.Column):
    def __init__(self, page: ft.Page, lesson_id):
        super().__init__()
        self.page = page
        self.lesson_id = lesson_id

    def build(self):
        self.controls=[]
        for p in db.get_tasks_by_lesson(self.page, self.lesson_id):
            print(p)
            self.controls.append(Task(self.page, p, self))

    def rebuild(self):
        self.build()
        self.update()