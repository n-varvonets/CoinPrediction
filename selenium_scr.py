from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_path = "C:\\Users\\User\\PycharmProjects\\CoinPrediction\\driver\\chromedriver.exe"
driver = webdriver.Chrome(service=Service(chromedriver_path))

URL = 'https://coinmarketcap.com/ru/'
driver.get(URL)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cmc-table')))

table = driver.find_element(By.CLASS_NAME, 'cmc-table')
rows = table.find_elements(By.TAG_NAME, 'tr')

for row in rows:
    try:
        rank_element = row.find_element(By.XPATH, './/td[@style="text-align:start"]')
        rank = rank_element.text.strip()
    except:
        rank = "Неизвестно"

    try:
        name_element = row.find_element(By.CLASS_NAME, 'cmc-link')
        coin_name = name_element.text.strip()
    except:
        coin_name = "Неизвестно"

    try:
        ticker_element = row.find_element(By.CLASS_NAME, 'coin-item-symbol')
        coin_ticker = ticker_element.text.strip()
    except:
        coin_ticker = "Неизвестно"

    percent_elements = row.find_elements(By.CLASS_NAME, 'sc-a59753b0-0.cmnujh')

    per_hour = "Нет данных"
    per_day = "Нет данных"
    per_week = "Нет данных"

    if len(percent_elements) >= 3:
        per_hour = percent_elements[0].text.strip()
        per_day = percent_elements[1].text.strip()
        per_week = percent_elements[2].text.strip()

    print(f'Ранг: {rank}, Криптовалюта: {coin_name} ({coin_ticker}), '
          f'Изменение за 1 час: {per_hour}, Изменение за 24 часа: {per_day}, Изменение за 7 дней: {per_week}')

driver.quit()
