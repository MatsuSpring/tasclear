import flet as ft
import sqlite3
import datetime

AppName = 'MyToDo(仮)'
DatabaseName = 'main.db'

class taskField(ft.Row):
    def __init__(self, properties):
        super().__init__()
        self.taskId = properties[0]
        self.taskName = properties[1]
        self.taskDeadlineSecond = properties[2]
        self.taskDeadline = datetime.datetime.fromtimestamp(self.taskDeadlineSecond)
        self.taskCompleted = properties[3]

        self.controls=[
            ft.Checkbox(value=self.taskCompleted, on_change=self.onCompletedChenged),
                ft.Column(
                    controls=[
                        ft.Text(value=self.taskName),
                        ft.Text(str(self.taskDeadline.year)+'年'+str(self.taskDeadline.month)+'月'+str(self.taskDeadline.day)+'日'+str(self.taskDeadline.hour)+'時'+str(self.taskDeadline.minute)+'分')
                    ]
                )
        ]
    
    def onCompletedChenged(self, e):
        co = sqlite3.connect(DatabaseName)
        cu = co.cursor()
        print('UPDATE tasks SET completed={} WHERE id={}'.format(e.control.value, self.taskId))
        cu.execute('UPDATE tasks SET completed={} WHERE id={}'.format(e.control.value, self.taskId))
        co.commit()
        co.close()

        

def main(page: ft.Page):
    conn = sqlite3.connect(DatabaseName)
    cur = conn.cursor()

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
    
    tf = taskField(cur.fetchall()[0])

    page.add(tf)
    
ft.app(main)
