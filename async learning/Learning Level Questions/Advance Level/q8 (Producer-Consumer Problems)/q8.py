# Implement a producer-consumer pattern
# Use asyncio.Queue to implement a producer-consumer system where the producer generates numbers every second, and the consumer processes them.

import random 
import asyncio

async def producer(queue):
    """Produces numbers and put them in the queue"""
    for _ in range(10): # Produces 10 numbers
        num = random.randint(1, 100)
        print(f"Producer: Generated {num}")
        await queue.put(num) # add the number to the queue
        await asyncio.sleep(1) # Simulate a delay (1 second)
    print("Producer : Done producing!")
    await queue.put(None) # Indicate the end of production


async def consumer(queue):
    """Consumes numbers from the queue and process them"""
    while True:
        num = await queue.get() # get a number from the queue
        if num is None: # Check for end-of-production singnal
            break
        print(f"Consumer: Processing {num}")
        await asyncio.sleep(2) # Simulate processing delay (2 seconds)

    print("Consumer: Done consuming!")




async def main():
    queue = asyncio.Queue() # create an asyncio.Queue

    # Run producer and consumer concurrently
    await asyncio.gather(
        producer(queue),
        consumer(queue)
    )

# Run the main coroutine
asyncio.run(main())