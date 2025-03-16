# Awaiting a coroutine
# What happens if you try to call a coroutine using my_coroutine() without await or asyncio.run()?

"""If you call a coroutine like my_coroutine() without using await or asyncio.run(), the coroutine does not execute. Instead, it simply returns a coroutine object

### What does this mean?
A coroutine object is essentially a "placeholder" or "promise" for the result of the coroutine. However, the actual function body of the coroutine will not run until the coroutine is awaited or executed within an event loop.
"""
# Example:
import asyncio
async def my_coroutine():
    print("Hello from the coroutine!")


# calling the coroutine with await or asyncio.run()

result = my_coroutine()
print(result)
# Output...
# <coroutine object my_coroutine at 0x00000245B5851300>
# sys:1: RuntimeWarning: coroutine 'my_coroutine' was never awaited
