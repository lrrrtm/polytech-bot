# todo: тут будет функция для парсинга списка групп
from bs4 import BeautifulSoup
from requests import get


def parse_groups_list():
    result_data = []

    url = f"https://ruz.spbstu.ru/search/groups?q=%2F"

    try:
        data = get(url=url, timeout=10)
    except Exception as e:
        return None

    soup = BeautifulSoup(data.text, "html.parser")
    groups = soup.find_all("a", {"class": "groups-list__link"})

    for group in groups:
        group_data = {
            'name': group.text,
            'faculty': group.attrs["href"].split("/")[-3],
            'group': group.attrs["href"].split("/")[-1]
        }

        result_data.append(group_data)

    return result_data
