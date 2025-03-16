import asyncio
import random

async def fetch_data(source):
    print(f"Fetching data from {source}...")
    delay = random.randint(1, 10)  # Random delay between 1 and 10 seconds
    await asyncio.sleep(delay)  # Simulate network delay
    print(f"Data received from {source} with delay of {delay} seconds")
    return f"Data from {source} = {delay * 5}"

async def fetch_with_timeout(source, timeout):
    try:
        # Use asyncio.wait_for to enforce a timeout
        return await asyncio.wait_for(fetch_data(source), timeout=timeout)
    except asyncio.TimeoutError:
        print(f"TimeoutError: Fetching data from {source} exceeded {timeout} seconds!")
        return f"Timeout fetching data from {source}"

async def main():
    tasks = [
        fetch_with_timeout("Server 1", timeout=2),
        fetch_with_timeout("Server 2", timeout=2),
        fetch_with_timeout("Server 3", timeout=2),
    ]

    # Run all tasks concurrently and collect results
    results = await asyncio.gather(*tasks)

    print("\nAll tasks completed!")
    print("Results:", results)

# Run the main coroutine
asyncio.run(main())
