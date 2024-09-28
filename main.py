import requests
from bs4 import BeautifulSoup

URL = 'https://coinmarketcap.com/ru/'

# Запрашиваем HTML контент страницы
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Найти таблицу с криптовалютами
table = soup.find('table', {'class': 'cmc-table'})  # Найти таблицу с нужным классом
if table:
    rows = table.find('tbody').find_all('tr')  # Найти все строки внутри таблицы
    for row in rows:
        # Найти ранговый номер криптовалюты (айди)
        rank_element = row.find('td', {'style': 'text-align:start'})
        rank = rank_element.text.strip() if rank_element else "Неизвестно"

        # Найти название криптовалюты
        name_element = row.find('a', class_='cmc-link')  # Используем <a> элемент с классом 'cmc-link'
        coin_name = name_element.text.strip() if name_element else "Неизвестно"

        # Найти тикер криптовалюты (например, BTC, ETH)
        ticker_element = row.find('p', {'class': 'coin-item-symbol'})
        coin_ticker = ticker_element.text.strip() if ticker_element else "Неизвестно"

        # Найти процентные изменения
        percent_elements = row.find_all('span', {'class': 'sc-a59753b0-0 cmnujh'})

        # Объявим переменные для хранения процентных изменений
        per_hour = "Нет данных"
        per_day = "Нет данных"
        per_week = "Нет данных"

        # Проверим, что все необходимые элементы найдены
        if len(percent_elements) >= 3:
            per_hour = percent_elements[0].text.strip()  # За 1 час
            per_day = percent_elements[1].text.strip()  # За 24 часа
            per_week = percent_elements[2].text.strip()  # За 7 дней

        # Выводим результат
        print(f'Ранг: {rank}, Криптовалюта: {coin_name} ({coin_ticker}), '
              f'Изменение за 1 час: {per_hour}, Изменение за 24 часа: {per_day}, Изменение за 7 дней: {per_week}')
else:
    print("Таблица не найдена")
