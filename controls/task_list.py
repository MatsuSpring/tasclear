import flet as ft
import database as db
from controls.task import Task

class TaskList(ft.Column):
    def __init__(self, lesson_id):
        super().__init__()
        self.lesson_id = lesson_id

    def build(self):
        self.controls=[]
        for p in db.get_tasks_by_lesson(self.lesson_id):
            print(p)
            self.controls.append(Task(p, self))

    def rebuild(self):
        self.build()
        self.update()
