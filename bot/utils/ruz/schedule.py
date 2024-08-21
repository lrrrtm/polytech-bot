import datetime

from bs4 import BeautifulSoup
from requests import get


def get_week_schedule(type: str, params: dict, date: datetime.date) -> dict:
    """
    Получение расписания на всю неделю
    :param type: тип расписания (group - для группы, teacher - для преподавателя)
    :param params: данные (faculty, groups для группы | teacher_id для преподавателя)
    :param date: дата любого дня дня требуемой недели

    :return:
    :response: True, если get status_code == 200, иначе False
    :general_info: номер группы/ФИО преподавателя
    :schedule: расписание в формате {<дата>: <расписание>}
    """
    if type == "group":
        url = f"https://ruz.spbstu.ru/faculty/{params['faculty']}/groups/{params['groups']}?date={date.strftime('%Y-%m-%d')}"
    else:
        url = f"https://ruz.spbstu.ru/teachers/{params['teacher_id']}?date={date.strftime('%Y-%m-%d')}"
    try:
        data = get(url=url, timeout=3)
    except Exception as e:
        return {'response': False}

    soup = BeautifulSoup(data.text, "html.parser")

    result_data = {
        'response': True,
        'general_info': {
            'name': soup.find('li', attrs={'class': 'breadcrumb-item active'}).text,
            'url': url
        },
        'schedule': {}
    }

    if len(soup.find_all('li', attrs={"class": "schedule__empty"})) == 1:  # расписания на неделю нет
        return result_data
    else:
        all_week = soup.find_all('li', attrs={'class': 'schedule__day'})
        for day_schedule in all_week:
            soup = BeautifulSoup(str(day_schedule), 'html.parser')

            cur_day = soup.find('div', attrs={'class': 'schedule__date'}).text[:2]
            cur_day_date = datetime.datetime.strptime(f'{date.year}-{date.month}-{cur_day}', '%Y-%m-%d')
            # cur_day_date = datetime.date(year=date.year, month=date.month, day=int(cur_day))
            lessons = soup.find_all('li', attrs={'class': 'lesson'})

            formatted_day_schedule = []
            for l in lessons:
                data = dict()
                soup = BeautifulSoup(str(l), 'html.parser')
                lesson_date_name = soup.find('div', attrs={'class': 'lesson__subject'})
                data['time'] = {
                    'start': cur_day_date + datetime.timedelta(hours=int(lesson_date_name.text[:2]),
                                                               minutes=int(lesson_date_name.text[3:5])),
                    'end': cur_day_date + datetime.timedelta(hours=int(lesson_date_name.text[6:8]),
                                                             minutes=int(lesson_date_name.text[9:11])),
                }

                data['name'] = lesson_date_name.text[12:]
                data['type'] = soup.find('div', attrs={'class': 'lesson__type'}).text
                data['teacher'] = {
                    'name': soup.find('div', attrs={'class': 'lesson__teachers'}).text if soup.find('div', attrs={
                        'class': 'lesson__teachers'}) else None,
                    'id': None
                }
                data['places'] = soup.find('div', attrs={'class': 'lesson__places'}).text
                formatted_day_schedule.append(data)
            result_data['schedule'][cur_day_date.date()] = formatted_day_schedule

        return result_data


def get_teacher_location(teacher_id: int):
    # current_date = datetime.datetime.now().date()
    current_date = datetime.datetime(year=2024, month=9, day=2, hour=9, minute=0)
    schedule = get_week_schedule(
        type="teacher",
        params={'teacher_id': teacher_id},
        date=current_date
    )

    if schedule['response']:  # запрос выполнен
        result = {'status': 'empty', 'lesson': None, 'teacher_name': schedule['general_info']['name'], 'url': schedule['general_info']['url']}

        if current_date.date() in schedule['schedule'].keys():  # сегодня есть занятия
            today_schedule = schedule['schedule'][current_date.date()]

            for lesson in today_schedule:
                if current_date < lesson['time']['start']:  # будет занятие
                    result['status'] = 'upcoming'
                    result['lesson'] = lesson
                    break
                elif lesson['time']['start'] <= current_date < lesson['time']['end']:
                    result['status'] = 'running'
                    result['lesson'] = lesson
                    break
        return True, result
    else:
        return False, {}
