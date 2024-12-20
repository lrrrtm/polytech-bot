import schedule
import time
from dotenv import load_dotenv
from os import getenv

from utils.parsers.groups import parse_groups_list
from utils.parsers.teachers import parse_teachers_list
from utils.parsers.saver import save_parsed_data

load_dotenv()

update_time = f"0{getenv('UPDATER_HOUR', 1)}:00"


def groups_list_updater():
    print('groups_list_updater started...')
    data = parse_groups_list()
    if data is not None:
        save_parsed_data(
            data=data,
            data_type='groups',
        )


def teachers_list_updater():
    print('teachers_list_updater started...')
    data = parse_teachers_list()
    if data is not None:
        save_parsed_data(
            data=data,
            data_type='teachers',
        )


schedule.every().day.at(update_time).do(groups_list_updater)
schedule.every().day.at(update_time).do(teachers_list_updater)

if bool(int(getenv(('DEVMODE')))):
    print(schedule.get_jobs())
    groups_list_updater()
    # teachers_list_updater()

while True:
    schedule.run_pending()
    time.sleep(1)
