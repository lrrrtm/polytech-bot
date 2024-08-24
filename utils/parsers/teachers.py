from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# todo: помечать преподов с идентичными ФИО, добавляя в конец их имени id

def parse_teachers_list():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=options)

    data = []

    try:
        driver.get('https://ruz.spbstu.ru/search/teacher?q=%20')
        pages_count = int(driver.find_elements(By.CLASS_NAME, 'pager__text')[0].text.split()[-1])
        for _ in range(pages_count - 1):
            teachers = driver.find_elements(By.CLASS_NAME, 'search-result__link')
            for teacher in teachers:
                teacher_data = {
                    'name': teacher.text,
                    'id': teacher.get_attribute('href').split('/')[-1]
                }
                data.append(teacher_data)
            next_button = driver.find_element(By.CLASS_NAME, 'fa.fa-arrow-circle-right')
            next_button.click()
        return data

    finally:
        driver.close()
        driver.quit()
