import json
from datetime import datetime


def save_parsed_data(data: list, data_type: str):
    paths = {
        'groups': "D:\Projects\polytech_bot\parsed_data\groups.json",
        'teachers': "D:\Projects\polytech_bot\parsed_data\\teachers.json"
    }

    with open(paths[data_type], 'w') as file:
        dump_data = {
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data': data
        }
        json.dump(dump_data, file, indent=4, ensure_ascii=False)
