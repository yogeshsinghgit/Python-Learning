## Use Case:
This approach is incredibly useful when working with I/O-bound tasks (e.g., network requests or database queries) where responses might take an unpredictable amount of time. The timeout ensures that your program does not hang indefinitely.

Would you like to explore other variations, such as retrying timed-out tasks

### **🔹 `asyncio.wait_for()` Explained**  

`asyncio.wait_for()` is used to **set a timeout on an async task**. If the task **takes longer than the specified timeout**, it raises an `asyncio.TimeoutError`.  

---

### **🚀 Basic Syntax**
```python
await asyncio.wait_for(coroutine, timeout)
```
- `coroutine` → The async function to run.  
- `timeout` → Maximum time (in seconds) before raising `asyncio.TimeoutError`.  
- If the coroutine **finishes within the timeout**, it returns normally.  
- If it **exceeds the timeout**, it raises an exception.  

---

## **🔥 Example: Handling Timeout in an Async Task**
```python
import asyncio

async def long_task():
    """Simulates a long-running task"""
    print("Task started...")
    await asyncio.sleep(5)  # Simulating a long operation (5 sec)
    print("Task completed!")
    return "✅ Task Finished"

async def main():
    try:
        result = await asyncio.wait_for(long_task(), timeout=3)  # ⏳ Set timeout to 3 sec
        print(result)
    except asyncio.TimeoutError:
        print("❌ Timeout! Task took too long.")

asyncio.run(main())  # Run the async function
```

---

### **✅ Expected Output**
#### **Case 1: Task Finishes Before Timeout (e.g., Task takes 2 sec, Timeout = 3 sec)**
```
Task started...
Task completed!
✅ Task Finished
```
✔ **No timeout** → The task finishes within the limit.  

#### **Case 2: Task Exceeds Timeout (e.g., Task takes 5 sec, Timeout = 3 sec)**
```
Task started...
❌ Timeout! Task took too long.
```
❌ **Timeout occurs** → The task is canceled, and `asyncio.TimeoutError` is raised.

---

## **📌 When to Use `asyncio.wait_for()`?**
| Scenario | Why Use `asyncio.wait_for()`? |
|----------|------------------------------|
| **API Requests** | Prevents waiting indefinitely for slow responses. |
| **Database Queries** | Avoids long-running queries from blocking execution. |
| **Background Tasks** | Ensures tasks don't run forever in async workflows. |
| **User Input/Operations** | Useful for setting deadlines for user actions. |
