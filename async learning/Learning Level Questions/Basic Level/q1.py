# # Define a coroutine
# Write a coroutine named hello_coroutine that prints "Hello, Async!", waits for 2 seconds, and then prints "Coroutine Finished".

definition = """A coroutine is a special type of asynchronous function in Python, designed to allow tasks to run concurrently without blocking the program's execution. Unlike traditional synchronous functions (defined using the def keyword), coroutines are defined using the async def syntax. They are executed with mechanisms like the await keyword, which pauses the coroutine until the awaited task is completed, or asyncio.run(), which is used to run the coroutine at the top level."""

import asyncio

async def hello_coroutine():
    print("Hello, Async!")
    await asyncio.sleep(2)
    print("Coroutine Finished")


asyncio.run(hello_coroutine())
