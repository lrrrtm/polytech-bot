import json

from bs4 import BeautifulSoup
from requests import get


# todo: объединить функции в одну

def get_groups_list(search_query: str) -> list:
    """
    Поиск групп по значению search_query
    :param search_query: строка поиска
    :return:
    :result_data: список найденных групп
    """

    with open("D:\Projects\polytech_bot\parsed_data\groups.json", encoding="utf-8") as file:
        groups_list = json.load(file)
        groups_list = groups_list['data']

    result_data = []
    for group in groups_list:
        if search_query in group['name']:
            result_data.append(
                {
                    'name': group['name'],
                    'faculty': group['faculty'],
                    'groups': group['group'],
                }
            )

    return result_data


def get_teachers_list(search_query: str):
    """
        Поиск преподавателей по значению search_query
        :param search_query: строка поиска
        :return:
        :result_data: список найденных преподавателей
        """
    with open("D:\Projects\polytech_bot\parsed_data\\teachers.json", encoding="utf-8") as file:
        teachers_list = json.load(file)
        teachers_list = teachers_list['data']

    result_data = []
    for teacher in teachers_list:
        if search_query in teacher['name']:
            result_data.append(
                {
                    'name': teacher['name'],
                    'id': teacher['id'],
                }
            )

    return True, result_data
