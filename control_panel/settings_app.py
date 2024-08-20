import flet as ft
from dotenv import load_dotenv

load_dotenv()


def main(page: ft.Page):
    page.title = "Настройки бота"

    page.window_width = 390
    page.window_height = 844

    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    page.theme = ft.Theme(
        # color_scheme=ft.ColorScheme(
        #     primary="#38b349",
        #     primary_container=ft.colors.GREEN_200
        # ),
    )

    page.add(
        ft.Column(
            [
                ft.Column(
                    [
                        ft.Text("Основные", size=25),
                        ft.TextField(label="Имя", hint_text="Введи своё имя", value="Артём", prefix_icon=ft.icons.ACCOUNT_CIRCLE),
                        ft.TextField(label="Группа", hint_text="Введи номер группы", value="5130904/20002", prefix_icon=ft.icons.GROUPS),
                    ]
                ),
                ft.Column(
                    [
                        ft.Text("Уведомления", size=25),
                        ft.Container(
                            ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Switch(value=False),
                                        title=ft.Text("Изменения в расписании"),
                                        subtitle=ft.Text("Напишем тебе, если в расписании на ближайшую неделю что-то поменяется")
                                    ),
                                    ft.ListTile(
                                        leading=ft.Switch(value=False),
                                        title=ft.Text("Следующая пара"),
                                        subtitle=ft.Text(
                                            "Отправим информацию о следующей паре за 15 минут до её начала")
                                    ),
                                    ft.ListTile(
                                        leading=ft.Switch(value=False),
                                        title=ft.Text("Технические сообщения"),
                                        subtitle=ft.Text(
                                            "Расскажем о новом функционале бота и предупредим о временном отключении")
                                    )
                                ]
                            ),
                            padding=ft.padding.only(left=-15)
                        )
                    ]
                ),
            ]
        )
    )

    page.update()


if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir='assets'
    )
