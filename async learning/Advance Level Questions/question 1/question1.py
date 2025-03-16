# Basic API and DB Coroutine Questions
# 1. Fetch Data from an API Asynchronously
# Write a coroutine fetch_data(url) that:

# Uses aiohttp to send a GET request to the provided url.
# Waits for the response.
# Returns the response data as JSON.
# 👉 Bonus: Fetch data from three different URLs concurrently using asyncio.gather().

#  Why Use aiohttp?

# ✅ Faster than requests (Non-blocking).
# ✅ Handles multiple requests efficiently.
# ✅ Best for web scraping, APIs, microservices.


import asyncio
import aiohttp

async def fetch_data(url):
    """Fetch data from an API asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json() # convert response to JSON
            print(f"Fetch data from {url}")
            return data
        

async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ]

    # Fetch all URLs concurrently
    results = await asyncio.gather(*(fetch_data(url) for url in urls))

    print("\nAll API requests completed.")
    print(results) # print all responses


# Run the async event loop/ main coroutine
asyncio.run(main())

