# # Run a coroutine
# How do you run a coroutine named my_coroutine() in Python?

"""To run a coroutine like my_coroutine() in Python, you typically need an event loop, which manages the execution of asynchronous tasks."""

# using asyncio.run() -> Preffered for top-level coroutines

"""Here, top-level signifies as the main entry point of your program, the part of your code that is executed first when you run the script. Esentially, It's the highest level in the hierarchy of function calls."""

"""Top-level coroutines are those that you want to run directly as the main task of your script.

Using asyncio.run() simplifies things by creating an event loop, running the coroutine, and managing everything automatically."""

import asyncio

async def my_coroutine():
    print("Running Coroutine!")

# Run the coroutine
asyncio.run(my_coroutine())