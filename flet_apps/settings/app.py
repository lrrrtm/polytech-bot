import os
import time
from urllib.parse import urlparse, parse_qs

import flet as ft
from dotenv import load_dotenv

from bot.utils.ruz.lists import get_groups_list
from bot.utils.ruz.other import get_group_name
from flet_apps.settings.dialogs import InfoDialog
from models.database import Database
from models.redis_s import Redis

load_dotenv()


def main(page: ft.Page):
    page.title = "Политехник"

    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    db = Database()
    rd = Redis()

    info = InfoDialog(page)

    def get_card_title(text: str) -> ft.Text:
        return ft.Text(
            value=text,
            size=20,
            weight=ft.FontWeight.W_400
        )

    def set_user_data(user_data: dict):
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

        db.update_user_notification_statuses(
            page.session.get('tid'),
            str(int(schedule_update_sw.value)),
            str(int(lesson_reminder_sw.value)),
            str(int(service_msg_sw.value)),
        )

    def group_redactor(e: ft.ControlEvent):
        action = e.control.data['action']

        if action == 'edit_group':
            e.control.icon = ft.icons.SAVE
            e.control.tooltip = "Сохранить"
            e.control.data['action'] = "save_group"
            user_group.read_only = False
            user_group.focus()

        elif action == 'save_group':
            new_group_name = user_group.value.strip()

            groups_list = get_groups_list(search_query=new_group_name)

            if len(groups_list) == 0:
                info.open("Редактирование", f"Группа {new_group_name} не найдена, попробуй ещё раз.")
            elif groups_list[0] is not None and len(groups_list) == 1:
                db.edit_user_group(page.session.get('tid'), int(groups_list[0]['faculty']),
                                   int(groups_list[0]['groups']))
                e.control.icon = ft.icons.EDIT
                e.control.tooltip = "Изменить группу"
                e.control.data['action'] = "edit_group"
                user_group.read_only = True
                info.open("Редактирование", f"Твоя группа изменена на {new_group_name}.")

            elif groups_list[0] is not None and len(groups_list) > 1:
                info.open("Редактирование",
                          f"Найдено несколько групп, в которых есть часть {new_group_name}, введи точный номер своей группы.")

            elif groups_list[0] is None:
                info.open("Ошибка", f"Ошибка связи с сервером, попробуй ещё раз.")

        page.update()

    def show_info_dialog(text: str, show_btn: bool = True):
        page.dialog = ft.AlertDialog(
            modal=True,
            title=get_card_title("Настройки"),
            content=ft.Text(
                value=text,
                size=16
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda _: close_dlg(loading_dialog), visible=show_btn),
            ]
        )
        page.dialog.open = True
        page.update()

    def open_dlg(dialog: ft.AlertDialog):
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dlg(dialog: ft.AlertDialog):
        dialog.open = False
        page.dialog = None
        page.update()

    loading_dialog = ft.AlertDialog(
        modal=True,
        title=get_card_title("Загрузка"),
        content=ft.ProgressBar()
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
                                content=user_group,
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                data={'action': "edit_group"},
                                tooltip="Изменить группу",
                                on_click=group_redactor
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
                                ),
                                ft.ListTile(
                                    leading=ft.Switch(),
                                    title=ft.Text("Наличие пышек"),
                                    subtitle=ft.Text(
                                        "Временно недоступно"
                                    ),
                                    disabled=True
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

    schedule = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    get_card_title("Расписание"),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.STAR),
                        title=ft.Text("Избранное"),
                        subtitle=ft.Text("Временно недоступно"),
                        on_click=lambda _: print("123"),
                        disabled=True
                    )
                ]
            ),
            padding=15
        )
    )

    settings_col = ft.Column(
        controls=[
            general_info,
            notifications,
            schedule
        ]
    )

    if bool(int(os.getenv(('DEVMODE')))):
        page.window.width = 390
        page.window.height = 844
        page.route = f"/settings?tid={409801981}&token={'devmode'}"
        tid = '409801981'
        token = 'devmode'

    else:
        parsed_url = urlparse(page.route)
        params = parse_qs(parsed_url.query)

        tid = params.get('uid', [None])[0]
        token = params.get('token', [None])[0]

    token_status = check_access_token(tid, token)
    if token_status == 'exists':
        open_dlg(loading_dialog)
        user = db.get_user_by_tid(int(tid))
        notifications_data = db.get_user_notifications_statuses(int(tid))

        user_data = {
            'general': {
                'group': get_group_name(user.faculty, user.group),
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
        close_dlg(loading_dialog)

    elif token_status == 'wrong':
        show_info_dialog(
            text="Изменение настроек доступно только внутри бота."
        )

    elif token_status == 'empty':
        show_info_dialog(
            text="Эта кнопка больше не работает, нажми на «Настройки» в боте ещё раз."
        )

    page.update()


if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir='assets',
        port=8502,
        view=None
    )
