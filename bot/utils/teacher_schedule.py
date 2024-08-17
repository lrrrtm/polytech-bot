from bs4 import BeautifulSoup
from requests import get


def give_teachers_list(search_query: str) -> list:
    try:
        data = get(url=f"https://ruz.spbstu.ru/search/teacher?q={search_query}", timeout=3)
    except Exception as e:
        return [None]

    soup = BeautifulSoup(data.text, "html.parser")
    teachers_list = soup.find_all("a", {"class": "search-result__link"})

    result_data = []
    for teacher in teachers_list:
        result_data.append(
            {
                'name': teacher.text,
                'href': teacher.attrs["href"].split("/")[-1],
            }
        )

    return result_data
