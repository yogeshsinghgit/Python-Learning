# Enhanced API Fetcher with Error Handling
# We'll add: ✔ Timeout Handling using asyncio.TimeoutError.
# ✔ HTTP Error Handling (400, 500, etc.).
# ✔ Retries for Failures (up to 3 times).

import asyncio
import aiohttp

async def fetch_data(url, session, retries = 3, timeout = 5):
    """Fetch data from an API asynchronously with error handling."""
    for attempt in range(1, retries+1):
        try:
            async with session.get(url, timeout = timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Success: {url}")
                    return data
                else:
                    print(f"Error {response.status}: {url}")
                    return None

        except asyncio.TimeoutError:
            print(f"Timeout on {url} (Attempt {attempt}/{retries})")
        except aiohttp.ClientError as e:
            print(f"Network Error on {url} : {e}")

    print(f"Failed after {retries} attempts: {url}")
    return None

async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/invalid-url"  # Invalid URL for testing
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(url, session) for url in urls]
        results = await asyncio.gather(*tasks)

    print("\nFinal Results:")
    for idx, result in enumerate(results, start=1):
        print(f"Post {idx}: {result['title'] if result else 'Failed'}")


asyncio.run(main())