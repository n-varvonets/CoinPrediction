import requests

URL = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing'

coins_data = []
start = 1
limit = 100  # Maximum number of records per request

while True:
    params = {
        'start': start,
        'limit': limit,
        'sortBy': 'market_cap',
        'sortType': 'desc',
        'convert': 'USD',
        'cryptoType': 'all',
        'tagType': 'all',
        'audited': False,
    }

    response = requests.get(URL, params=params)
    data = response.json()

    if data['status']['error_code'] == '0':
        cryptocurrencies = data['data']['cryptoCurrencyList']

        if not cryptocurrencies:
            break  # If there are no more data, exit the loop

        for coin in cryptocurrencies:
            coin_data = {}
            coin_data['rank'] = coin.get('cmcRank', 'Unknown')
            coin_data['name'] = coin.get('name', 'Unknown')
            coin_data['ticker'] = coin.get('symbol', 'Unknown')
            coin_data['slug'] = coin.get('slug', '')
            coin_data['href'] = f"https://coinmarketcap.com/currencies/{coin_data['slug']}/"

            # Get percentage changes
            quotes = coin.get('quotes', [])
            if quotes:
                usd_quote = quotes[0]
                coin_data['percent_change_1h'] = usd_quote.get('percentChange1h', 0)
                coin_data['percent_change_24h'] = usd_quote.get('percentChange24h', 0)
                coin_data['percent_change_7d'] = usd_quote.get('percentChange7d', 0)
            else:
                coin_data['percent_change_1h'] = coin_data['percent_change_24h'] = coin_data['percent_change_7d'] = 0

            coins_data.append(coin_data)

        print(f"Retrieved data from cryptocurrency {start} to {start + len(cryptocurrencies) - 1}")

        start += limit  # Increase the starting value for the next request

    else:
        print("Error retrieving data:", data['status']['error_message'])
        break

# Now we have the full list of cryptocurrencies in coins_data
print(f"Total cryptocurrencies retrieved: {len(coins_data)}")

# Output all cryptocurrencies (you can comment this out if not needed)
# '''
for coin in coins_data:
    print(f"Rank: {coin['rank']}, Cryptocurrency: {coin['name']} ({coin['ticker']}), "
          f"24h Change: {coin['percent_change_24h']}%, "
          f"Link: {coin['href']}")
# '''

# Find the top 5 cryptocurrencies by 24h change
# Sort the list by 'percent_change_24h' in descending order
top_5 = sorted(coins_data, key=lambda x: x['percent_change_24h'], reverse=True)[:5]

print("\nTop 5 cryptocurrencies by 24h change:")
for idx, coin in enumerate(top_5, start=1):
    print(f"{idx}. {coin['name']} ({coin['ticker']}): 24h Change: {coin['percent_change_24h']}%, Link: {coin['href']}")
