# Fetch Crypto Prices from CoinGecko

import asyncio
import aiohttp

async def fetch_crypto_prices(url):
    """Fetch data from an API asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json() # COnvert response to JSON
                print(f"Data fetched from {url}")
                return data
            else:
                print(f"Error {response.status} fetching {url}")
                return None
            

async def main():
    base_url = "https://api.coingecko.com/api/v3/simple/price"
    cryptos = ["bitcoin", "ethereum", "dogecoin"]
    params = "?ids=" + ",".join(cryptos) + "&vs_currencies=usd"

    url = base_url + params

    # Fetch data asynchronosly
    result = await fetch_crypto_prices(url)

    if result:
        print("\nLive Crypto Prices:")
        for coin, price in result.items():
            print(f"{coin.capitalize()}: ${price['usd']}")


asyncio.run(main())