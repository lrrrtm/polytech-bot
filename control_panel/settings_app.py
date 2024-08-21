import os
import time
from urllib.parse import urlparse, parse_qs

import flet as ft
from dotenv import load_dotenv

from models.database import Database
from models.redis_s import Redis

load_dotenv()


def main(page: ft.Page):
    page.title = "Политехник"

    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    db = Database()
    rd = Redis()

    def get_card_title(text: str) -> ft.Text:
        return ft.Text(
            value=text,
            size=20,
            weight=ft.FontWeight.W_400
        )

    def set_user_data(user_data: dict):
        user_name.value = user_data['general']['name']
        user_group.value = user_data['general']['group']
        user_tid.value = user_data['general']['tid']

        schedule_update_sw.value = user_data['notifications']['schedule_update']
        lesson_reminder_sw.value = user_data['notifications']['lesson_reminder']
        service_msg_sw.value = user_data['notifications']['service_message']

    def check_access_token(key: str, value: str):
        original = rd.get_value(key)
        if original is None:
            status = 'empty'
        else:
            original = original.decode('utf-8')
            if original == value:
                status = 'exists'
            elif original != value:
                status = 'wrong'

        return status

    def notification_switch_changed(e: ft.ControlEvent):
        switch_statuses = {
            True: {
                'caption': "Уведомление подключено",
                'bgcolor': ft.colors.GREEN
            },
            False: {
                'caption': "Уведомление отключено",
                'bgcolor': ft.colors.AMBER
            }
        }

        db.update_user_notification_statuses(
            page.session.get('tid'),
            str(int(schedule_update_sw.value)),
            str(int(lesson_reminder_sw.value)),
            str(int(service_msg_sw.value)),
        )

        page.snack_bar = ft.SnackBar(
            content=ft.Text(
                size=16,
                value=switch_statuses[e.control.value]['caption'],
            ),
            bgcolor=switch_statuses[e.control.value]['bgcolor']
        )
        page.snack_bar.open = True
        page.update()

    def change_name(e: ft.ControlEvent):
        print(e.control.data)
        type = e.control.data

        if type == "edit":
            user_name.read_only = False
            e.control.data = "save"
            e.control.icon = ft.icons.SAVE
            e.control.tooltip = "Сохранить"
            user_name.focus()

        elif type == "save":
            user_name.read_only = True
            e.control.data = "edit"
            e.control.icon = ft.icons.EDIT
            e.control.tooltip = "Изменить имя"

            db.edit_user_name(
                page.session.get('tid'),
                user_name.value.strip(),
            )

            page.snack_bar = ft.SnackBar(
                content=ft.Text("Имя изменено"),
                bgcolor=ft.colors.GREEN
            )
            page.snack_bar.open = True

        page.update()

    def show_info_dialog(text: str, show_btn: bool = True):
        page.dialog = ft.AlertDialog(
            modal=True,
            title=get_card_title("Настройки"),
            content=ft.Text(
                value=text,
                size=16
            )
        )
        page.dialog.open = True
        page.update()

    user_name = ft.TextField(
        icon=ft.icons.ACCOUNT_CIRCLE,
        label="Имя",
        read_only=True
    )

    user_group = ft.TextField(
        icon=ft.icons.GROUP,
        label="Учебная группа",
        read_only=True
    )

    user_tid = ft.TextField(
        icon=ft.icons.TELEGRAM,
        label="Telegram ID",
        read_only=True
    )

    general_info = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    get_card_title("Основное"),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=user_name,
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Изменить имя",
                                data="edit",
                                on_click=change_name
                            )
                        ],
                        width=page.width
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=user_group,
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Изменить группу",
                                on_click=None
                            )
                        ],
                        width=page.width
                    ),
                    user_tid
                ]
            ),
            padding=15
        )
    )

    switch_active_color = ft.colors.GREEN
    schedule_update_sw = ft.Switch(active_color=switch_active_color, on_change=notification_switch_changed,
                                   data='schedule_update')
    lesson_reminder_sw = ft.Switch(active_color=switch_active_color, on_change=notification_switch_changed,
                                   data='lesson_reminder')
    service_msg_sw = ft.Switch(active_color=switch_active_color, on_change=notification_switch_changed,
                               data='service_message')

    notifications = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    get_card_title("Уведомления"),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.ListTile(
                                    leading=schedule_update_sw,
                                    title=ft.Text("Изменения в расписании"),
                                    subtitle=ft.Text(
                                        "Напишем тебе, если в расписании на ближайшие 7 дней что-то поменяется")
                                ),
                                ft.ListTile(
                                    leading=lesson_reminder_sw,
                                    title=ft.Text("Следующая пара"),
                                    subtitle=ft.Text(
                                        "Отправим информацию о следующей паре за 15 минут до её начала")
                                ),
                                ft.ListTile(
                                    leading=service_msg_sw,
                                    title=ft.Text("Технические сообщения"),
                                    subtitle=ft.Text(
                                        "Расскажем о новом функционале и предупредим о временном отключении бота")
                                )
                            ]
                        ),
                        padding=ft.padding.only(left=-15)
                    )

                ]
            ),
            padding=15
        )
    )

    settings_col = ft.Column(
        controls=[
            general_info,
            notifications
        ]
    )

    if bool(os.getenv(('DEVMODE'))):
        page.window.width = 390
        page.window.height = 844
        tid = 409801981

    page.route = f"/settings?tid={409801981}&token={'devmode'}"
    parsed_url = urlparse(page.route)
    params = parse_qs(parsed_url.query)

    tid = params.get('tid', [None])[0]
    token = params.get('token', [None])[0]

    token_status = check_access_token(tid, token)
    if token_status == 'exists':
        user = db.get_user_by_tid(int(tid))
        notifications_data = db.get_user_notifications_statuses(int(tid))

        user_data = {
            'general': {
                'name': user.name,
                'group': user.group,
                'tid': user.tid
            },
            'notifications': {
                'schedule_update': bool(int(notifications_data.schedule_corrections)),
                'lesson_reminder': bool(int(notifications_data.schedule_notify)),
                'service_message': bool(int(notifications_data.service_msgs))
            }
        }

        set_user_data(user_data)
        page.session.set('tid', tid)
        page.add(settings_col)

    elif token_status == 'wrong':
        show_info_dialog(
            text="У вас отсутствует разрешение на просмотр настроек данного пользователя"
        )

    elif token_status == 'empty':
        show_info_dialog(
            text="Срок токена соединения истёк, нажми на кнопку «Настройки» в боте ещё раз."
        )
        print('TOKEN STATUS EMPTY')

    page.update()


if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir='assets'
    )
