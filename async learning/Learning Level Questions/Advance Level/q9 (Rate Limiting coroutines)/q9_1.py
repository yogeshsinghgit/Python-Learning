# Rate-limiting coroutines
# Write an async function that ensures only 3 tasks run concurrently using asyncio.Semaphore().

import asyncio, random

async def limited_task(semaphore, task_id):
    """A task that acquires a semaphore to limit concurrency"""
    async with semaphore:
        print(f"Task {task_id} is starting...")
        await asyncio.sleep(random.randint(1, 5)) # Simulates some work with random delay
        print(f"Task {task_id} has completed!")
        return task_id


async def main():
    semaphore = asyncio.Semaphore(3) # Liit to 3 concurrent tasks
    tasks = []

    # create 10 tasks
    # tasks = [asyncio.create_task(limited_task(i, semaphore)) for i in range(1, 11)]
    for i in range(1,11):
        tasks.append(limited_task(semaphore, i))

    # Run all tasks concurrently while respecting the semaphore limit
    results = await asyncio.gather(*tasks)

    print(results)

# Run the main coroutine
asyncio.run(main())