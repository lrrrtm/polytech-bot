from aiogram.utils import markdown

yandex_form_link = markdown.hlink("эту форму", "https://forms.yandex.ru/u/66c0f6d42530c215f5889e54/")



lexicon = {
    'cmd_about': "<b>Политехник</b> - это неофициальный бот политехнического университета Петра Великого, "
                 "созданный и поддерживаемый студентами."
                 "\n\nС помощью бота ты можешь удобно смотреть расписание своей группы, "
                 "получать уведомления о внезапных изменениях в нём, искать преподавателей и многое другое"
                 f"\n\nЕсли у тебя есть предложения по функционалу бота или рекламы, заполни {yandex_form_link}"
                 "\n\nСоздатели бота: @lrrrtm и @simonoffcc",
    'menu_find_teacher': "<b>🧑‍🏫 Поиск преподавателя</b>"
                         "\n\nЗдесь ты можешь определить, где находится преподаватель согласно его расписанию."
                         "\n\nДля этого отправь фамилию или полное ФИО преподавателя.",
    'cmd_help': "<b>Расписание и функции</b>\n"
                "/schedule - меню расписания\n"
                "/selected_schedule - избранное\n"
                "/find_teacher - найти препода\n"
                "/buildings - корпуса\n\n"
                "<b>Настройки</b>\n"
                "/settings - настройки (WebApp)\n\n"
                "<b>Бот</b>\n"
                "/start - начать\n"
                "/menu - меню\n"
                "/help - команды\n\n"
                "/about - <b>о боте и разработчиках</b>\n\n"
                f"\n\n{markdown.hblockquote("Если ты видишь это сообщение, не использовав команду /help, "
                                            "значит ты отправил сообщение, на которое бот никак корректно не реагирует."
                                            "\n\nЕсли ты считаешь, что это ошибка, то заполни форму по ссылке ниже.")}"
                f"\n--- {yandex_form_link} ---",
    'cmd_menu': "<b>Главное меню</b> 🏡",
    'hello': "Привет! Это неофициальный бот политеха, с помощью которого ты можешь просматривать расписание занятий, "
             "искать преподавателей и другую информацию."
             "\n\nОтправь номер своей группы, чтобы я мог показывать тебе твоё расписание."
             f"\n\n{markdown.hblockquote('Пример номера группы: 5130904/20002. '
                                         'Если знаешь только часть номера, отправь её и выбери точный номер '
                                         'из предложенных вариантов')}"
}
