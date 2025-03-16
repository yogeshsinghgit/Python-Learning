import asyncio
import random

async def fetch_data(api_name, delay):
    """Simulates fetching data from an API with variable delay."""
    print(f"📡 {api_name} request started... (Expected delay: {delay} sec)")
    await asyncio.sleep(delay)  # Simulates API response time
    return f"✅ {api_name} response received"

async def main():
    try:
        # Setting different timeouts for each API request
        task1 = asyncio.wait_for(fetch_data("API-1", random.randint(1, 5)), timeout=2)
        task2 = asyncio.wait_for(fetch_data("API-2", random.randint(1, 5)), timeout=4)
        task3 = asyncio.wait_for(fetch_data("API-3", random.randint(1, 5)), timeout=3)

        # Run all tasks concurrently
        results = await asyncio.gather(task1, task2, task3, return_exceptions=True)

        # Handling results
        for i, result in enumerate(results, start=1):
            if isinstance(result, asyncio.TimeoutError):
                print(f"❌ API-{i} timed out!")
            else:
                print(result)

    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")

asyncio.run(main())  # Run the main function
