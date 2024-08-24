import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в безголовом режиме
chrome_options.add_argument("--no-sandbox")  # Для устранения проблем с правами доступа
chrome_options.add_argument("--disable-dev-shm-usage")  # Для устранения проблем с памятью
chrome_options.add_argument("--window-size=1920x1080")  # Задайте размер окна

driver = webdriver.Chrome()

data = []

try:
    driver.get('https://ruz.spbstu.ru/search/teacher?q=%20')

    while True:
        # Находим все элементы с ФИО преподавателей
        teachers = driver.find_elements(By.CLASS_NAME, 'search-result__link')
        for teacher in teachers:
            teacher_data = {
                'name': teacher.text,
                'id': teacher.get_attribute('href').split('/')[-1]
            }
            data.append(teacher_data)

        # Пытаемся перейти на следующую страницу
        try:
            next_button = driver.find_element(By.CLASS_NAME, 'fa.fa-arrow-circle-right')
            next_button.click()
            # time.sleep(0.5)  # Задержка для загрузки новой страницы
        except Exception as e:
            print("Нет больше страниц или ошибка:", e)
            break  # Выходим из цикла

finally:
    driver.close()
    driver.quit()
    with open("data.json", "w") as f:
        json.dump(data, f)
