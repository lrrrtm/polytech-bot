# Процессор для получения информации о расписании группы или преподавателя
# Для запуска необходимы beautifulsoup4, pydantic, requests

from typing import List, Dict
import requests

from bs4 import BeautifulSoup
from pydantic.v1 import BaseModel
import datetime

GROUP_SCHEDULE_URL = "https://ruz.spbstu.ru/faculty/{0}/groups/{1}?date={2}"
TEACHER_SCHEDULE_URL = "https://ruz.spbstu.ru/teachers/{0}?date={1}"
AUDITORY_SCHEDULE_URL = "https://ruz.spbstu.ru{0}?date={1}"


class ScheduleElementAuditory(BaseModel):
    """Описывает информацию по аудитории элемента расписания"""

    name: str
    url: str


class ScheduleElementTeacher(BaseModel):
    """Описывает информацию о преподавателе"""

    name: str | None
    url: str | None


class ScheduleElementTiming(BaseModel):
    """Описывает временной диапазон элемента расписания"""

    start_date: datetime.datetime | datetime.date = None
    end_date: datetime.datetime | datetime.date = None


class ScheduleElementLink(BaseModel):
    """Описывает объект внешней ссылки занятия (СДО, Вебинар, etc)"""

    title: str
    url: str


class ScheduleElement(BaseModel):
    """Описывает элемент расписания"""

    name: str | None
    type: str | None
    timing: ScheduleElementTiming
    teacher: ScheduleElementTeacher | None
    auditory: ScheduleElementAuditory | None
    links: List[ScheduleElementLink] = []


class DayScheduleElement(BaseModel):
    """Описывает объект расписания на весь день"""

    timing: ScheduleElementTiming
    lessons: List[ScheduleElement] = []


class WeekScheduleElement(BaseModel):
    """Описывает объект расписания на всю неделю"""

    timing: ScheduleElementTiming
    days: List[DayScheduleElement] = []


months_captions = {
    'янв.': 1,
    'фев.': 2,
    'мар': 3,
    'апр.': 4,
    'мая': 5,
    'июн.': 6,
    'июл.': 7,
    'авг.': 8,
    'сент.': 9,
    'окт.': 10,
    'нояб.': 11,
    'дек.': 12,
}


def get_week_dates_list(request_date: datetime.date) -> dict:
    """
    Возвращает список дат недели по заданному дню
    :param request_date:
    :return: datetime.date понедельника
    """
    start_of_week = request_date - datetime.timedelta(days=request_date.weekday())

    week_dates = {start_of_week + datetime.timedelta(days=i): False for i in range(7)}

    return week_dates


def fetch_week_schedule(volume: str, volume_data: dict, request_date: datetime.date) -> WeekScheduleElement | None:
    """
    Получает всё расписание на всю неделю по заданной дате
    :param request_date: заданная дата
    :param volume: раздел поиска (teacher, group)
    :param volume_data: словарь данных {teacher_id: int} или {faculty: int, group: int}
    :return: WeekScheduleElement | None
    """

    week_days = get_week_dates_list(request_date=request_date)

    if volume == 'group':
        url = GROUP_SCHEDULE_URL.format(volume_data['faculty'], volume_data['group'], request_date.strftime('%Y-%m-%d'))

    elif volume == 'teacher':
        url = TEACHER_SCHEDULE_URL.format(volume_data['teacher_id'], request_date.strftime('%Y-%m-%d'))

    page = requests.get(
        url=url
    )

    if page.status_code == 200:
        week_schedule = WeekScheduleElement(
            timing=ScheduleElementTiming()
        )

        soup = BeautifulSoup(page.text, "html.parser")
        schedule_days = soup.find_all('li', class_='schedule__day')

        # проходимся по всем дням в текущей неделе
        for index, day in enumerate(schedule_days):

            time = day.find('div', class_='schedule__date')
            day_date_formatted = datetime.date(
                year=request_date.year,
                month=int(months_captions[time.text.split(' ')[1][:-1]]),
                day=int(time.text.split(' ')[0]),
            )

            # print(day_date_formatted, week_days)
            if day_date_formatted in week_days.keys():
                week_days[day_date_formatted] = True
            else:
                print(f"{day_date_formatted} not in {week_days.keys()}")

            day_schedule_element = DayScheduleElement(
                timing=ScheduleElementTiming(
                    start_date=day_date_formatted,
                    end_date=day_date_formatted
                )
            )

            # задаём дату начала и дату окончания недели по первому и последнему дню
            if index == 0:
                week_schedule.timing.start_date = day_date_formatted
            elif index == len(schedule_days) - 1:
                week_schedule.timing.end_date = day_date_formatted

            for lesson in day.find_all('li', class_='lesson'):
                subject_and_time = lesson.find('div', class_='lesson__subject')
                lesson_time, lesson_name = subject_and_time.text.split(" ")[0], ' '.join(
                    subject_and_time.text.split(" ")[1:])

                start_time = lesson_time.split("-")[0]
                end_time = lesson_time.split("-")[1]

                f_time = ScheduleElementTiming(
                    start_date=datetime.datetime(
                        year=day_date_formatted.year,
                        month=day_date_formatted.month,
                        day=day_date_formatted.day,
                        hour=int(start_time.split(":")[0]),
                        minute=int(start_time.split(":")[1])
                    ),
                    end_date=datetime.datetime(
                        year=day_date_formatted.year,
                        month=day_date_formatted.month,
                        day=day_date_formatted.day,
                        hour=int(end_time.split(":")[0]),
                        minute=int(end_time.split(":")[1])
                    ),

                )

                lesson_type = lesson.find('div', class_='lesson__type')

                lesson_teacher = lesson.find('div', class_='lesson__teachers')

                if lesson_teacher and len(lesson_teacher.text.strip().split(' ')) > 1:
                    lesson_teacher_link = TEACHER_SCHEDULE_URL.format(
                        lesson_teacher.find('a', class_='lesson__link').get('href').split('/')[-1],
                        day_date_formatted
                    )
                    lesson_teacher = lesson_teacher.text.strip()
                else:
                    lesson_teacher_link = None
                    lesson_teacher = None

                f_teacher = ScheduleElementTeacher(
                    name=lesson_teacher,
                    url=lesson_teacher_link,
                )

                lesson_place = lesson.find('div', class_='lesson__places')
                lesson_place_link = lesson_place.find('a')['href']
                lesson_place_link = AUDITORY_SCHEDULE_URL.format(lesson_place_link, day_date_formatted)

                f_place = ScheduleElementAuditory(
                    name=lesson_place.text,
                    url=lesson_place_link
                )

                lesson_links = []
                links = lesson.find('div', class_='lesson__resource_links')
                if links:
                    for link in links:
                        lesson_links.append(
                            ScheduleElementLink(
                                title=link.find('a').text,
                                url=link.find('a')['href']
                            )
                        )

                f_lesson = ScheduleElement(
                    name=lesson_name,
                    type=lesson_type.text,
                    timing=f_time,
                    teacher=f_teacher,
                    auditory=f_place,
                    links=lesson_links
                )

                day_schedule_element.lessons.append(f_lesson)

        for date, is_exist in week_days.items():
            if is_exist is False:
                week_schedule.days.append(
                    DayScheduleElement(
                        timing=ScheduleElementTiming(
                            start_date=date,
                            end_date=date
                        )
                    )
                )

        week_schedule.days.sort(key=lambda x: x.timing.start_date)
        return week_schedule

    return None


def get_schedule_by_date(volume: str, volume_data: dict, request_date: datetime.date) -> DayScheduleElement | None:
    """
    Возвращает расписание на заданный день или None, если расписания нет
    :param request_date: заданная дата
    :param volume: раздел поиска (teacher, group)
    :param volume_data: словарь данных {teacher_id: int} или {faculty: int, group: int}
    :return: DayScheduleElement | None
    """

    # получаем расписание на всю неделю
    week_schedule = fetch_week_schedule(
        volume=volume,
        volume_data=volume_data,
        request_date=request_date
    )

    # если расписание на неделю вернулось, проверяем наличие нужного дня в неделе, если его нет, отдаём None
    if week_schedule:
        filtered_data = list(filter(lambda x: x.timing.start_date == request_date, week_schedule.days))
        if filtered_data:
            return filtered_data[0]

    return None


if __name__ == "__main__":
    # Тестовое получение расписания группы по заданном дню
    group_schedule_response = get_schedule_by_date(
        volume='group',
        volume_data={
            'faculty': 125,
            'group': 40518,
        },
        request_date=datetime.date(
            year=2024,
            month=11,
            day=24
        )
    )

    print(group_schedule_response)

    print("-" * 75)

    # Тестовое получение расписания преподавателя по заданном дню
    teacher_schedule_response = get_schedule_by_date(
        volume='teacher',
        volume_data={
            'teacher_id': 22154
        },
        request_date=datetime.date(
            year=2024,
            month=11,
            day=24
        )
    )

    print(teacher_schedule_response)
