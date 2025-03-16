# Task cancellation and error handling in asynchronous content using asyncio.create_task()

import asyncio
import random

async def fetch_data(source):
    try:
        print(f"Fetching data from {source}...")
        delay = random.randint(1, 10)
        await asyncio.sleep(delay) # Simulate network delay
        if delay > 5: # simulate an error for demonstration
            raise Exception(f"Timeout fetching data from source {source}")
        
        print(f"Data received from {source} with delay of {delay}")
        return f"Data from {source} = {delay*5}"
    
    except asyncio.CancelledError:
        print(f"Fetching from {source} was cancelled!")
        return f"{source} fetch cancelled"

    except Exception as e:
        print(f"Error occured: {e}")
        return f"Error fetching data from {source} : {e}"
    

async def main():
    # Create tasks.
    task1 = asyncio.create_task(fetch_data("Server 1"))
    task2 = asyncio.create_task(fetch_data("Server 2"))
    task3 = asyncio.create_task(fetch_data("Server 3"))
    
    # Introduce cancellation for one task after a dealy.
    await asyncio.sleep(3)
    print("Cancelling server 2 fetch...")
    task2.cancel() # Cancel task2

    # Wait for all tasks to complete (handling cancellations and errors)
    results = await asyncio.gather(task1, task2, task3, return_exceptions=True)

    print("\nALl tasks completed!")
    print("Results: ", results)


# Run the main coroutine
asyncio.run(main())