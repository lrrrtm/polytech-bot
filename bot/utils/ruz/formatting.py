from datetime import datetime

location_statuses = {
    'running': {
        'caption': "Идёт занятие"
    },
    'upcoming': {
        'caption': "Занятие запланировано"
    },
    'empty': {
        'caption': "Занятия не запланированы"
    }
}


def get_block_for_location(location_data) -> str:
    text_block = f"🧑‍🎓 {location_data['teacher_name']}"

    caption = location_statuses[location_data['status']]['caption']
    text_block += f"\n💡 {caption}"

    if location_data['status'] != 'empty':
        lesson = location_data['lesson']
        text_block += (f"\n\n<b>{lesson['name']}</b>"
                       f"\n⏰ {datetime.strftime(lesson['time']['start'], '%H:%M')}-"
                       f"{datetime.strftime(lesson['time']['end'], '%H:%M')}"
                       f"\n📚 {lesson['type']}"
                       f"\n📍 {lesson['places']}")

    return text_block
