### **🔹 What is `asyncio.Semaphore()`?**  
A **semaphore** is a synchronization **mechanism** that limits the number of concurrent tasks that can access a shared resource at the same time. In `asyncio`, `Semaphore` is used to **control the number of coroutines running concurrently**.  

This is useful when:  
✅ You are making **many API requests** but need to limit them to avoid rate limits.  
✅ You are performing **database operations** but want to prevent too many concurrent connections.  
✅ You need to **throttle tasks** to prevent overloading a system.

---

## **🔹 How `asyncio.Semaphore()` Works**
A semaphore starts with a counter (e.g., `asyncio.Semaphore(3)`) that represents **how many tasks can run at the same time**.  
- **When a coroutine starts**, it **acquires** the semaphore (`await semaphore.acquire()`).  
- **When it finishes**, it **releases** the semaphore (`semaphore.release()`).  
- If the limit is reached, new coroutines **must wait** until a slot is available.

---

## **🔹 Example: Controlling API Requests with `asyncio.Semaphore()`**
```python
import asyncio
import random

semaphore = asyncio.Semaphore(3)  # Limit: Only 3 coroutines can run at once

async def fetch_data(task_id):
    async with semaphore:  # Automatically acquires & releases semaphore
        print(f"Task {task_id} started...")
        await asyncio.sleep(random.uniform(1, 3))  # Simulate API request
        print(f"Task {task_id} completed!")

async def main():
    tasks = [fetch_data(i) for i in range(10)]  # 10 tasks
    await asyncio.gather(*tasks)

asyncio.run(main())
```

### **🔹 Expected Output (Order May Vary)**
```
Task 0 started...
Task 1 started...
Task 2 started...
Task 0 completed!
Task 3 started...
Task 1 completed!
Task 4 started...
Task 2 completed!
Task 5 started...
...
```
- At most **3 tasks run at the same time** (due to `Semaphore(3)`).
- As soon as one finishes, the next task **takes its place**.

---

## **🔹 When to Use `asyncio.Semaphore()`**
✅ **API Rate Limiting** (e.g., only 5 requests at a time).  
✅ **Database Connections** (e.g., prevent exceeding DB connection pool size).  
✅ **File Processing** (e.g., limit the number of files read concurrently).  

---

### **🔹 Alternative: Using `asyncio.BoundedSemaphore()`**
`asyncio.BoundedSemaphore()` works like `Semaphore`, but **prevents releasing more times than it was acquired** (helps avoid accidental over-releases).

```python
semaphore = asyncio.BoundedSemaphore(3)
```
