import json
from datetime import datetime
from os import getenv


def save_parsed_data(data: list, data_type: str):
    paths = {
        'groups': fr"{getenv('ABSOLUTE_PROJECT_FOLDER')}\parsed_data\groups.json",
        'teachers': fr"{getenv('ABSOLUTE_PROJECT_FOLDER')}\parsed_data\teachers.json"
    }

    with open(paths[data_type], 'w') as file:
        dump_data = {
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data': data
        }
        json.dump(dump_data, file, indent=4, ensure_ascii=False)
