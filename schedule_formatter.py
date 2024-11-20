"""Форматирует полученную информацию schedule_processor.py в текст для телеграм."""

import emoji

from typing import List
import datetime
from schedule_processor import DayScheduleElement, ScheduleElement, ScheduleElementTiming  # Импортируйте ваши модели

import locale
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)

class ScheduleFormatter:
    """Форматирует расписание для вывода в Telegram или текстовом виде."""

    @staticmethod
    def format_day_schedule(day_schedule: DayScheduleElement) -> str:
        """
        Форматирует расписание на день в читаемый текст.

        :param day_schedule: Объект расписания на день.
        :return: Отформатированное расписание.
        """
        if not day_schedule.lessons:
            return "На этот день занятий нет."

        formatted_lessons = []
        for lesson in day_schedule.lessons:
            formatted_lessons.append(ScheduleFormatter.format_lesson(lesson))

        # Заголовок с датой
        day_title = (f"{emoji.emojize(":calendar:")} Расписание на "
                     f"{day_schedule.timing.start_date.strftime('%d.%m.%y')} "
                     f"({day_schedule.timing.start_date.strftime('%A')})\n")

        return day_title + "\n" + "\n\n".join(formatted_lessons)

    @staticmethod
    def format_lesson(lesson: ScheduleElement) -> str:
        """
        Форматирует один элемент занятия.

        :param lesson: Объект занятия.
        :return: Отформатированная строка занятия.
        """
        # Время занятия
        time_range = f"{lesson.timing.start_date.strftime('%H:%M')}–{lesson.timing.end_date.strftime('%H:%M')}"

        # Название и тип занятия
        name_and_type = f"{lesson.name} ({lesson.type})"

        # Преподаватель
        teacher = f"{emoji.emojize(":teacher:")} {lesson.teacher.name}" if lesson.teacher.name \
            else f"{emoji.emojize(":teacher:")} Преподаватель не указан"

        # Аудитория
        auditory = f"{emoji.emojize(":round_pushpin:")} {lesson.auditory.name}" if lesson.auditory.name \
            else f"{emoji.emojize(":round_pushpin:")} Место проведения не указано"

        # Ссылки
        links = ""
        if lesson.links:
            links_list = "\n".join([f"{emoji.emojize(":link:")} [{link.title}]({link.url})" for link in lesson.links])  # todo: проследить, что сообщение отправляется в markdown
            links = f"\n{links_list}"

        return f"{emoji.emojize(":alarm_clock:")} {time_range} {name_and_type}\n{teacher}\n{auditory}{links}"


if __name__ == '__main__':
    from schedule_processor import get_schedule_by_date

    day_schedule_response = get_schedule_by_date(
        volume='group',
        volume_data={
            'faculty': 125,
            'group': 40518,
        },
        request_date=datetime.date(
            year=2024,
            month=11,
            day=20
        )
    )

    formatted_day_schedule = ScheduleFormatter.format_day_schedule(day_schedule_response)
    print(formatted_day_schedule)
