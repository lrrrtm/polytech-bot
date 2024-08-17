from bs4 import BeautifulSoup
from requests import get


def get_groups_list(search_query: str) -> list:
    try:
        data = get(url=f"https://ruz.spbstu.ru/search/groups?q={search_query}", timeout=10)
    except Exception as e:
        return [None]

    soup = BeautifulSoup(data.text, "html.parser")
    teachers_list = soup.find_all("a", {"class": "groups-list__link"})

    result_data = []
    for teacher in teachers_list:
        result_data.append(
            {
                'name': teacher.text,
                'faculty': teacher.attrs["href"].split("/")[-3],
                'groups': teacher.attrs["href"].split("/")[-1],
            }
        )

    return result_data


print(get_groups_list('5132704'))
