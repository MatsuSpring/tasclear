import flet as ft


def main(page: ft.Page):
    page.theme_mode = 'light'
    theme = ft.Theme(
        color_scheme_seed=ft.colors.GREEN_500
    )
    page.theme = theme
    page.dark_theme = theme
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.FACT_CHECK_ROUNDED),
        leading_width=40,
        title=ft.Text('MyToDo'),
        center_title=True,
        bgcolor=theme.color_scheme_seed
    )


    page.add()
    
ft.app(main)
