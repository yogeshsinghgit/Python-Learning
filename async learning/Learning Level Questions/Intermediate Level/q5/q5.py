# Simulating an I/O-bound task
# Write a coroutine fetch_data() that simulates fetching data from a server by waiting for 3 seconds (await asyncio.sleep(3)) and then returning "Data received".

import asyncio

async def fetch_data():
    print("Fetching data from the servers...")
    await asyncio.sleep(3) # simulate a network delay of 3 seconds..
    return "Data received"


# result = asyncio.run(fetch_data())
# print(result)

# Or 


async def main():
    result = await fetch_data()  # Wait for the coroutine to complete
    print(result)

asyncio.run(main())  # Run the main coroutine