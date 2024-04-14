import flet as ft

AppName = 'MyToDo(仮)'

class taskField(ft.UserControl):
    def __init__(self, properties):
        taskId = properties[0]
        taskName = properties[1]
        taskDeadline = properties[2]
        taskCompleted = properties[3]
        


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


    page.add()
    
ft.app(main)
