

Here’s how you can write the coroutine `fetch_data()` to simulate an I/O-bound task in Python:

```python
import asyncio

async def fetch_data():
    print("Fetching data from the server...")
    await asyncio.sleep(3)  # Simulate a network delay of 3 seconds
    return "Data received"
```

### How It Works:
1. **`async def fetch_data()`**: Defines the coroutine.
2. **`await asyncio.sleep(3)`**: Pauses the coroutine for 3 seconds, simulating an I/O-bound delay such as fetching data from a remote server.
3. **Return Value**: After the delay, the coroutine returns `"Data received"`.

### To Run This Coroutine:
You need an event loop to execute it, such as:

```python
import asyncio

async def main():
    result = await fetch_data()  # Wait for the coroutine to complete
    print(result)

asyncio.run(main())  # Run the main coroutine
```

This will print:
```
Fetching data from the server...
Data received
```


---

### 1. **Direct `asyncio.run(fetch_data())` Approach**
```python
result = asyncio.run(fetch_data())
print(result)
```
- **Pros:**
  - Simple and concise, ideal for running a single coroutine.
  - Suitable for quick tasks or scripts where you only need to execute one coroutine directly.
- **Cons:**
  - If you need to run additional asynchronous tasks or organize your code into multiple coroutines, this approach can become unwieldy.
  - Less scalable for larger, more complex programs.

---

### 2. **`asyncio.run(main())` with a `main()` Coroutine**
```python
async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```
- **Pros:**
  - More flexible and modular: You can orchestrate multiple coroutines within `main()` or even call other async functions.
  - Easier to manage complex workflows (e.g., if you're awaiting multiple tasks or performing concurrent operations).
  - Code is cleaner and follows a structured approach, especially for larger applications.
- **Cons:**
  - Slightly more verbose for simple use cases.

---

### Which Is Better?
- **For Simple Tasks:** Use `asyncio.run(fetch_data())` when the program is limited to one coroutine and doesn't require modularity.
- **For Complex Programs:** Use `async def main()` with `asyncio.run(main())` for better code organization and scalability.

### Example Use Case for `main()`:
If you want to fetch data from multiple sources concurrently:
```python
async def main():
    task1 = fetch_data()
    task2 = fetch_data()
    results = await asyncio.gather(task1, task2)
    print(results)

asyncio.run(main())
```
This modular approach handles concurrency gracefully, which wouldn't be as clean with the first method.

## gather() vs create_task()

-> Use q5_1.py and q5_2.py for code reference.

Here's how you can modify the code to use `asyncio.create_task()` instead of `asyncio.gather()`:

### Modified Code:
```python
import asyncio
import random

async def fetch_data(source):
    print(f"Fetching data from {source}...")
    delay = random.randint(1, 10)
    await asyncio.sleep(delay)  # Simulate network delay
    print(f"Data received from {source} with delay of {delay}")
    return f"Data from {source} = {delay * 5}"

async def main():
    # Create tasks for each fetch operation
    task1 = asyncio.create_task(fetch_data("Server 1"))
    task2 = asyncio.create_task(fetch_data("Server 2"))
    task3 = asyncio.create_task(fetch_data("Server 3"))

    # Wait for tasks to complete and gather their results
    results = await asyncio.gather(task1, task2, task3)

    # Print the results
    print("All tasks completed!")
    print("Results:", results)

# Run the main coroutine
asyncio.run(main())
```

---

### Key Difference Between `asyncio.gather()` and `asyncio.create_task()`:

| **Aspect**                  | **`asyncio.gather()`**                                                                                      | **`asyncio.create_task()`**                                                                 |
|-----------------------------|-----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| **Purpose**                 | Directly runs multiple coroutines concurrently and waits for all of them to complete.                     | Wraps a coroutine in a `Task`, which can then be managed explicitly.                     |
| **Usage**                   | Combines multiple coroutines into one unified coroutine, which can be awaited.                            | Creates individual tasks that can run concurrently and independently.                    |
| **Return Value**            | Returns the results of all coroutines in a single step.                                                  | Requires manual aggregation of results, often with an additional tool like `await` or `asyncio.gather()`. |
| **Explicit Task Management** | Does not create explicit `Task` objects; operates directly on coroutines.                               | Creates `Task` objects, allowing for advanced management like cancellation or monitoring. |
| **Code Example Focus**       | High-level, simpler usage for running multiple coroutines concurrently.                                  | Flexible and modular, enabling finer control of individual tasks.                        |

---

### How They Differ in the Workflow:
1. **With `asyncio.gather()`**:
   - You pass the coroutine objects directly to `asyncio.gather()`, which runs them concurrently.
   - `asyncio.gather()` handles everything automatically, returning the results of all coroutines once they complete.
   - This is a clean and compact way to manage concurrent tasks.

2. **With `asyncio.create_task()`**:
   - Each coroutine is first turned into a `Task` using `asyncio.create_task()`, which schedules it for execution.
   - You can explicitly manage or monitor these tasks (e.g., by storing them in variables or cancelling them if needed).
   - You'll often combine `create_task()` with tools like `await` or `asyncio.gather()` to collect results.

---

### When to Use Each:
- **Use `asyncio.gather()`** when:
  - You simply want to run multiple coroutines concurrently and wait for all results.
  - You don't need to manage individual tasks or have fine-grained control over them.

- **Use `asyncio.create_task()`** when:
  - You need to create tasks that you can control individually (e.g., cancelling or inspecting the status of specific tasks).
  - You want tasks to start immediately but don't necessarily need to wait for all of them to complete in the same place.
