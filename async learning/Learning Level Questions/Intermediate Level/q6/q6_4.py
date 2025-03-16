# Combining q6_2 and q6_3 for better Version

about = """
🔥 Improvements in This Version
✅ Automatic Retries → If a request times out, it retries up to retries times.
✅ Custom Timeouts for Each Task → Each server has a different timeout limit.
✅ Better Logging → Clearly shows attempts and failures.
✅ Same Modular Design → fetch_with_timeout() remains reusable.
"""

import asyncio
import random

async def fetch_data(source):
    """Simulates fetching data from a remote server."""
    print(f"Fetching data from {source}...")
    delay = random.randint(1, 10)  # Random delay between 1-10 sec
    await asyncio.sleep(delay)  # Simulate network delay
    print(f"✅ Data received from {source} (delay: {delay} sec)")
    return f"Data from {source} = {delay * 5}"

async def fetch_with_timeout(source, timeout, retries=2):
    """Attempts to fetch data with timeout and retry logic."""
    for attempt in range(1, retries + 1):
        try:
            return await asyncio.wait_for(fetch_data(source), timeout=timeout)
        except asyncio.TimeoutError:
            print(f"⏳ Timeout! {source} attempt {attempt} exceeded {timeout} sec.")

    print(f"❌ Failed to fetch data from {source} after {retries} retries.")
    return f"Timeout fetching data from {source}"

async def main():
    tasks = [
        fetch_with_timeout("Server 1", timeout=3, retries=2),
        fetch_with_timeout("Server 2", timeout=4, retries=3),
        fetch_with_timeout("Server 3", timeout=2, retries=1),
    ]

    results = await asyncio.gather(*tasks)
    print("\n🎉 All tasks completed!")
    print("📌 Final Results:", results)

print(f"\n {about} \n")
asyncio.run(main())  # Run the async tasks
