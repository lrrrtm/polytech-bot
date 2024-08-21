from bs4 import BeautifulSoup
from requests import get


def get_group_name(faculty: int, groups: int):
    try:
        data = get(url=f"https://ruz.spbstu.ru/faculty/{faculty}/groups/{groups}", timeout=10)
    except Exception as e:
        return None

    soup = BeautifulSoup(data.text, "html.parser")
    group_name = soup.find('li', {'class': "breadcrumb-item active"})

    return group_name.text.split()[-1] if group_name else None