# Task cancellation
# Write a coroutine that starts a long-running task (asyncio.sleep(5)) but cancels it after 2 seconds.

import asyncio

async def long_running_task():
    print("Task Started")
    try: 
        await asyncio.sleep(5) # Simulate a long-running task
        print("Task Completed!")
    except asyncio.CancelledError:
        print("Task was cancelled!") # Handle task cancellation gracefully
        raise


async def main():
    # Staet the long-runningtask
    task = asyncio.create_task(long_running_task())

    # Wait for 2 seconds before cancelling the task
    await asyncio.sleep(2)
    print("Cancelling the task...")
    task.cancel() # Cancel the task

    # Handle the cancellation and ensure graceful completion
    # try:
    #     await task
    # except asyncio.CancelledError:
    #     print("Task cancellation acknowledged!")

# Run the main coroutine
asyncio.run(main())