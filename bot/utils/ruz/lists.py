from bs4 import BeautifulSoup
from requests import get


# to-do: объединить функции в одну

def get_groups_list(search_query: str) -> list:
    """
    Поиск групп по значению search_query
    :param search_query: строка поиска
    :return:
    :result_data: список найденных групп
    """
    try:
        data = get(url=f"https://ruz.spbstu.ru/search/groups?q={search_query}", timeout=10)
    except Exception as e:
        return [None]

    soup = BeautifulSoup(data.text, "html.parser")
    groups_list = soup.find_all("a", {"class": "groups-list__link"})

    result_data = []
    for group in groups_list:
        result_data.append(
            {
                'name': group.text,
                'faculty': group.attrs["href"].split("/")[-3],
                'groups': group.attrs["href"].split("/")[-1],
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
    try:
        data = get(url=f"https://ruz.spbstu.ru/search/teacher?q={search_query}", timeout=3)
    except Exception as e:
        return False, []

    soup = BeautifulSoup(data.text, "html.parser")
    teachers_list = soup.find_all("a", {"class": "search-result__link"})

    result_data = []
    for teacher in teachers_list:
        result_data.append(
            {
                'name': teacher.text,
                'id': teacher.attrs["href"].split("/")[-1],
            }
        )

    return True, result_data

