Explore the power of `asyncio.create_task()` by showcasing how to handle **task cancellation** and **error handling** in an asynchronous context.

---

### Example: Canceling Tasks and Handling Errors

```python
import asyncio
import random

async def fetch_data(source):
    try:
        print(f"Fetching data from {source}...")
        delay = random.randint(1, 10)
        await asyncio.sleep(delay)  # Simulate network delay
        if delay > 5:  # Simulate an error for demonstration
            raise Exception(f"Timeout fetching data from {source}")
        print(f"Data received from {source} with delay of {delay}")
        return f"Data from {source} = {delay * 5}"
    except asyncio.CancelledError:
        print(f"Fetching from {source} was cancelled!")
        return f"{source} fetch cancelled"
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Error fetching data from {source}: {e}"

async def main():
    # Create tasks
    task1 = asyncio.create_task(fetch_data("Server 1"))
    task2 = asyncio.create_task(fetch_data("Server 2"))
    task3 = asyncio.create_task(fetch_data("Server 3"))

    # Introduce cancellation for one task after a delay
    await asyncio.sleep(3)
    print("Cancelling Server 2 fetch...")
    task2.cancel()  # Cancel task2

    # Wait for all tasks to complete (handling cancellations and errors)
    results = await asyncio.gather(task1, task2, task3, return_exceptions=True)

    print("\nAll tasks completed!")
    print("Results:", results)

# Run the main coroutine
asyncio.run(main())
```

---

### Explanation:
1. **`asyncio.CancelledError`:**
   - This exception is caught to handle situations when a task is cancelled using `task.cancel()`.
   - The coroutine `fetch_data` gracefully handles the cancellation by printing a message.

2. **Simulated Error (`raise Exception`):**
   - A random delay is introduced, and any delay greater than 5 seconds raises an exception to simulate a timeout.

3. **`asyncio.gather(..., return_exceptions=True)`**:
   - This ensures that exceptions in individual tasks (like `CancelledError` or other errors) are returned instead of immediately propagating.
   - This makes the program robust, as all tasks complete even if some fail or are cancelled.

4. **Task Cancellation:**
   - `task2.cancel()` is used to cancel the task fetching data from "Server 2".

---

### Sample Output (Your results may vary due to random delays):
```
Fetching data from Server 1...
Fetching data from Server 2...
Fetching data from Server 3...
Cancelling Server 2 fetch...
Fetching from Server 2 was cancelled!
Error occurred: Timeout fetching data from Server 3
Data received from Server 1 with delay of 3

All tasks completed!
Results: ['Data from Server 1 = 15', 'Server 2 fetch cancelled', 'Error fetching data from Server 3: Timeout fetching data from Server 3']
```

---

This approach gives you fine-grained control over your asynchronous workflows.