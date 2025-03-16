# Multiple coroutines execution
# Write an async function that runs two coroutines (task1() and task2()) concurrently using asyncio.gather().

import asyncio

async def task1():
    print("Task 1, Started!")
    await asyncio.sleep(2)
    print("Task 1, Competed.")

async def task2():
    print("Task 2, Started!")
    await asyncio.sleep(2)
    print("Task 2, Competed.")


# tasks  = lambda task : asyncio.gather(task1(), task2())
# asyncio.run(tasks)

# ValueError: a coroutine was expected, got <_GatheringFuture pending>        
# sys:1: RuntimeWarning: coroutine 'task2' was never awaited
# sys:1: RuntimeWarning: coroutine 'task1' was never awaited

"""
Your error happens because asyncio.run() only accepts a coroutine, not a future or task.

* asyncio.gather(task1(), task2()) returns a future, not a coroutine.
* asyncio.run() requires a coroutine, not a future.
* The correct way is to wrap asyncio.gather() inside an async function.
"""

# correct code:

# Wrap asyncio.gather() inside an async def main() function, This ensures we pass a coroutine to asyncio.run().

async def main():
    await asyncio.gather(task1(), task2())  # ✅ Run both coroutines concurrently

# call asyncio.run(main()) at the top level
asyncio.run(main())