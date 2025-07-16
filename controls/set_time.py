import flet as ft
import datetime

class setTime(ft.Column):
    def __init__(self, t):
        super().__init__()
        self.dpYear = ft.Dropdown(
            width=207,
            options=[ft.dropdown.Option(i) for i in range(t.year, t.year+3)],
            value=t.year,
            text_size=18,
            content_padding=15,
        )
        self.dpMonth = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(1, 13)],
            value=t.month,
            text_size=18,
            content_padding=10,
        )
        self.dpDay = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(1, 32)],
            value=t.day,
            text_size=18,
            content_padding=10,
        )
        self.dpHour = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(0, 24)],
            value=t.hour,
            text_size=18,
            content_padding=10,
        )
        self.dpMin = ft.Dropdown(
            width=85,
            options=[ft.dropdown.Option(i) for i in range(0, 60)],
            value=t.minute,
            text_size=18,
            content_padding=10,
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
