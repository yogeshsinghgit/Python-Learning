# Handling coroutines with timeouts
# Modify the fetch_data() coroutine to raise a TimeoutError if it takes longer than 2 seconds using asyncio.wait_for()

import asyncio
import random

async def fetch_data():
    """Simulates fetching data with a random delay."""
    delay = random.randint(1, 4)  # Random delay between 1-4 seconds
    print(f"Fetching data... (Expected delay: {delay} sec)")
    await asyncio.sleep(delay)  # Simulates network delay
    return "Data Received"

async def main():
    try:
        result = await asyncio.wait_for(fetch_data(), timeout=2)  # Timeout set to 2 sec
        print(result)
    except asyncio.TimeoutError:
        print("Timeout! The request took too long.")

asyncio.run(main())  # Run the async function
