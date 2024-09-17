from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
# Запуск нового экземпляра браузера Chrome
browser = webdriver.Chrome()
# Переход на первую страницу веб-сайта
browser.get("https://www.spaceweatherlive.com/ru/arhiv/2011/01/01/xray.html")

# Инициализация пустого списка для хранения цитат
ratyng_year = []
count = 1

while True:
# Поиск всех цитат на странице с помощью xpath
    quote_elements = browser.find_elements(By.XPATH,'//div[contains(@class,"col-md-8 pb-5")]')
# Извлечение текста каждой цитаты
    for quote_element in quote_elements:
        date = quote_element.find_element(By.XPATH,'.//h3').text
        power = quote_element.find_element(By.XPATH,'.//div[8]/div/table/tbody/tr/td[4]').text
        ratyng_year.append({"date": date, "power": power})

# Проверка наличия следующей кнопки
    next_button = browser.find_elements(By.XPATH,'//div[contains(@class,"btn-group")]/div/a[1]')
# Нажатие следующей кнопки
    next_button[0].click()
# Ожидание загрузки страницы
    time.sleep(1)
    count += 1
    if count > 31:
        break

# Запись данных в файл CSV
with open("ratyng_1.csv", "w", encoding='UTF-8', newline="") as file: 
    writer = csv.DictWriter(file, fieldnames=["date", "power"])
    writer.writeheader()
    writer.writerows(ratyng_year)
# Закрытие браузера
browser.close()
