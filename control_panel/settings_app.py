import flet as ft
from dotenv import load_dotenv

from models.database import Database

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

    notification_changed_snack_bar = ft.SnackBar(
        content=ft.Text(size=16)
    )
    page.overlay.append(notification_changed_snack_bar)

    db = Database()

    def notifications_switched(e: ft.ControlEvent):
        statuses = {
            True: {
                'caption': "Уведомление подключено",
                'color': ft.colors.GREEN
            },
            False: {
                'caption': "Уведомление отключено",
                'color': ft.colors.AMBER
            }
        }

        # switch to db
        # send message
        data = db.get_user_notifications_statuses(tid=409801981)
        print(data.service_msgs, data.schedule_notify, data.schedule_corrections)

        notification_changed_snack_bar.content.value = statuses[e.control.value]['caption']
        notification_changed_snack_bar.bgcolor = statuses[e.control.value]['color']
        notification_changed_snack_bar.open = True
        page.update()

    page.add(
        ft.Column(
            [
                ft.Column(
                    [
                        ft.Text("Основные", size=25),
                        ft.TextField(label="Имя", hint_text="Введи своё имя", value="Артём",
                                     prefix_icon=ft.icons.ACCOUNT_CIRCLE),
                        ft.TextField(label="Группа", hint_text="Введи номер группы", value="5130904/20002",
                                     prefix_icon=ft.icons.GROUPS),
                    ]
                ),
                ft.Column(
                    [
                        ft.Text("Уведомления", size=25),
                        ft.Container(
                            ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Switch(
                                            value=False,
                                            active_color="#38b349",
                                            data={'type': 'schedule_corrections'},
                                            on_change=notifications_switched
                                        ),
                                        title=ft.Text("Изменения в расписании"),
                                        subtitle=ft.Text(
                                            "Напишем тебе, если в расписании на ближайшую неделю что-то поменяется")
                                    ),
                                    ft.ListTile(
                                        leading=ft.Switch(
                                            value=False,
                                            active_color="#38b349",
                                            data={'type': 'schedule_notify'},
                                            on_change=notifications_switched
                                        ),
                                        title=ft.Text("Следующая пара"),
                                        subtitle=ft.Text(
                                            "Отправим информацию о следующей паре за 15 минут до её начала")
                                    ),
                                    ft.ListTile(
                                        leading=ft.Switch(
                                            value=False,
                                            active_color="#38b349",
                                            data={'type': 'service_msgs'},
                                            on_change=notifications_switched
                                        ),
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
