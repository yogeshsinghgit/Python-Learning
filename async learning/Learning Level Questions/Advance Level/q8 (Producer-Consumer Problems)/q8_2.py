# Instead of numbers, you can put functions or coroutines in an asyncio.Queue. This allows you to use the queue to manage the execution of tasks dynamically. Here's how it can be done:

import asyncio

async def task_a():
    print("Executing Task A...")
    await asyncio.sleep(2)
    print("Task A completed!")

async def task_b():
    print("Executing Task B...")
    await asyncio.sleep(3)
    print("Task B completed!")

async def producer(queue):
    """Produces tasks (functions) and puts them in the queue."""
    print("Producer: Adding tasks to the queue...")
    await queue.put(task_a)  # Add the task_a function to the queue
    await queue.put(task_b)  # Add the task_b function to the queue
    await queue.put(None)  # Signal the consumer to stop
    print("Producer: Done producing tasks!")

async def consumer(queue):
    """Consumes tasks from the queue and executes them."""
    while True:
        task = await queue.get()  # Get a task from the queue
        if task is None:  # Check for the stop signal
            break
        print(f"Consumer: Starting a task...")
        await task()  # Execute the task (call the coroutine)
    print("Consumer: Done consuming tasks!")

async def main():
    queue = asyncio.Queue()

    # Run producer and consumer concurrently
    await asyncio.gather(
        producer(queue),
        consumer(queue),
    )

# Run the main coroutine
asyncio.run(main())
