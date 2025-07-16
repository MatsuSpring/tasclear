import flet as ft
import storage as db
from controls.task_field_tabs import taskFieldTabs

AppName = 'TasClear'

def main(page: ft.Page):
    page.title = AppName
    page.theme_mode = 'light'
    theme = ft.Theme(
        color_scheme_seed=ft.Colors.GREEN_400,
    )
    page.theme = theme
    page.dark_theme = theme
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED),
        leading_width=70,
        title=ft.Text(AppName),
        center_title=True,
        bgcolor=theme.color_scheme_seed
    )

    db.init_storage(page)

    tft = taskFieldTabs(page)

    page.add(tft)

    
ft.app(main)
