# Practcing Async Programming in Python
import asyncio


async def task1():
    print("Task 1 Started")
    await asyncio.sleep(2) # simulates an I/O operation
    print("Task 1 Completed")

async def task2():
    print("Task 2 Started")
    await asyncio.sleep(2) 
    print("Task 2 Completed")


async def main():
    # Run both tasks concurrently
    await asyncio.gather(task1(), task2())


# run the event loop
asyncio.run(main())

