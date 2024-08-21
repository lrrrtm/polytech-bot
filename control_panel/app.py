import flet as ft
from dotenv import load_dotenv

load_dotenv()


def main(page: ft.Page):
    page.title = "Панель администратора"
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER,
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#38b349",
            primary_container=ft.colors.GREEN_200
        ),
    )

    page.scroll = None

    card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.icons.ADMIN_PANEL_SETTINGS, size=200),
                    ft.TextField(hint_text="* * * * * *", text_align=ft.TextAlign.CENTER, width=300, height=50,
                                 password=True, border_radius=ft.border_radius.all(30)),
                    ft.FilledButton(text="Войти", width=300, height=50),
                    ft.Text("Панель администрирования ботом v0.1")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=15,
        ),
        width=450,
        height=600,
        elevation=10
    )

    page.add(ft.Container(card, expand=True, margin=ft.margin.symmetric(vertical=100)))


if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir='assets'
    )
