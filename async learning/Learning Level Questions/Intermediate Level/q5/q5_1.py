# enhance your coroutine by handling multiple simulated fetch requests concurrently using asyncio.gather(). This method allows you to run multiple coroutines simultaneously and wait for all of them to complete.

import asyncio
import random

async def fetch_data(source):
    print(f"Fetching data from {source}...")
    delay = random.randint(1, 10)
    await asyncio.sleep(delay) # Simulate network delay
    print(f"Data received from {source} with delay of {delay}")
    return f"Data from {source} = {delay*5}"

async def main():
    # Simulating multiple fetch request from different server
    tasks = [
        fetch_data("Server 1"),
        fetch_data("Server 2"),
        fetch_data("Server 3")
    ]

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)

    # print the results
    print("All tasks completed!")
    print("Results: ", results)



# Run the main coroutine
asyncio.run(main())