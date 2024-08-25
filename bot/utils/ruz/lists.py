import json
from os import getenv


def get_groups_list(search_query: str) -> list:
    with open(f"{getenv('ABSOLUTE_PROJECT_FOLDER')}\parsed_data\groups.json", encoding="utf-8") as file:
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
    with open(f"{getenv('ABSOLUTE_PROJECT_FOLDER')}\parsed_data\\teachers.json", encoding="utf-8") as file:
        teachers_list = json.load(file)
        teachers_list = teachers_list['data']

    search_query = search_query.lower()
    query_parts = search_query.split()

    matches = []

    for teacher in teachers_list:
        name = teacher['name'].lower()
        if all(part in name for part in query_parts):
            matches.append(teacher)

    return True, matches
