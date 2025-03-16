
# Using asyncio.create_task()

import asyncio
import random

async def fetch_data(source):
    print(f"Fetching data from {source}...")
    delay = random.randint(1, 10)
    await asyncio.sleep(delay)  # Simulate network delay
    print(f"Data received from {source} with delay of {delay}")
    return f"Data from {source} = {delay * 5}"


async def main():
    # Create tasks for each fetch operations
    task1 = asyncio.create_task(fetch_data("Server 1"))
    task2 = asyncio.create_task(fetch_data("Server 2"))
    task3 = asyncio.create_task(fetch_data("Server 3"))

    # Wait for tasks to complete and gather their results
    results = await asyncio.gather(task1, task2, task3)

    # Print the results
    print("All tasks completed")
    print("Results: ", results)



# Run the main coroutine
asyncio.run(main())