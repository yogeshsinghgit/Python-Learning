# README

## What is Couroutine?

Coroutines are a special kind of function in Python that allow for cooperative multitasking. Unlike regular functions, coroutines can be paused and resumed, making them useful for asynchronous programming.

### Key Features of Coroutines:

1. They use async def – Coroutines are defined using async def, making them different from normal functions.
2. They can be paused with await – This allows a coroutine to yield control back to the event loop while waiting for something (e.g., network response, I/O operation).
3. They enable concurrency without threads – Coroutines allow multiple tasks to run concurrently without creating multiple threads.

await does two things simultaneously:

1️⃣ Calls another coroutine / awaitable
2️⃣ Suspends the current coroutine until the awaited task finishes

So when Python reaches await, the coroutine pauses its execution and the event loop can run other coroutines.

Example :

``` python
import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# running the coroutine
asyncio.run(say_hello())
```

### **⏳ Why Not Use `time.sleep()` in Async Code?**  

In **asyncio-based code**, you should use **`await asyncio.sleep()` instead of `time.sleep()`** because:  

1. **`time.sleep()` blocks the entire event loop** ⛔  
   - It **pauses everything**, preventing other async tasks from running.  
   - This makes your program inefficient and **defeats the purpose of async programming**.  

2. **`await asyncio.sleep()` yields control back to the event loop** ✅  
   - It **doesn’t block** other tasks while waiting.  
   - The event loop can run other coroutines while waiting.  

---

### **🚀 Example: Blocking vs. Non-Blocking Sleep**
#### **❌ Using `time.sleep()` (Blocks Everything)**
```python
import asyncio
import time

async def async_task():
    print("Task started...")
    time.sleep(3)  # ❌ Blocks the whole event loop!
    print("Task completed!")

async def main():
    await async_task()  # This blocks everything for 3 sec
    print("Main function continues...")

asyncio.run(main())
```
🛑 **Bad** → The whole program **pauses for 3 seconds** before continuing.  

---

#### **✅ Using `await asyncio.sleep()` (Non-Blocking)**
```python
import asyncio

async def async_task():
    print("Task started...")
    await asyncio.sleep(3)  # ✅ Non-blocking, other tasks can run
    print("Task completed!")

async def main():
    task = asyncio.create_task(async_task())  # Run in background
    print("Main function continues...")
    await task  # Wait for task to finish

asyncio.run(main())
```
✅ **Good** → While waiting for `asyncio.sleep(3)`, the event loop **can run other tasks**.  

---

### **📌 TL;DR**
| **Function**          | **Blocking?** | **Freezes Event Loop?** | **Use in Async Code?** |
|----------------------|-------------|------------------|----------------|
| `time.sleep(3)`     | ✅ Yes      | ❌ Yes (bad)     | ❌ No |
| `await asyncio.sleep(3)` | ❌ No  | ✅ No (good) | ✅ Yes |

💡 **Use `await asyncio.sleep()` in async functions to avoid blocking the event loop!** 🚀


---


## What is Event Loop?

An **event loop** is the core mechanism in **asynchronous programming** that continuously monitors and executes pending tasks, such as I/O operations, timers, and coroutines. It enables Python to handle multiple tasks **concurrently** without creating multiple threads.

### **How the Event Loop Works**
1. **Starts Running:** The event loop waits for tasks (coroutines) to execute.
2. **Executes Tasks:** It picks up pending coroutines and runs them **until they reach an `await` statement**.
3. **Handles Awaited Tasks:** If a coroutine is waiting for an operation (e.g., network request, file read), the event loop pauses it and moves to the next task.
4. **Resumes Paused Tasks:** Once the awaited operation is complete, the event loop resumes the paused coroutine where it left off.
5. **Repeats the Process:** This continues until all tasks are completed.

---

### **Example of an Event Loop in Python**
```python
import asyncio

async def task1():
    print("Task 1 started")
    await asyncio.sleep(2)  # Simulates an I/O operation
    print("Task 1 completed")

async def task2():
    print("Task 2 started")
    await asyncio.sleep(1)
    print("Task 2 completed")

async def main():
    # Run both tasks concurrently
    await asyncio.gather(task1(), task2())

# Run the event loop
asyncio.run(main())
```

**Expected Output (order may vary due to concurrency):**
```
Task 1 started
Task 2 started
Task 2 completed
Task 1 completed
```
- The event loop starts and runs `task1()` and `task2()` **concurrently**.
- `task1()` waits for 2 seconds (`await asyncio.sleep(2)`), while `task2()` only waits for 1 second.
- The event loop does **not block** while waiting for the sleep functions; it allows other coroutines to run.

---

### **Key Features of the Event Loop**
✅ **Single-threaded but concurrent** – It does not create new threads but still runs tasks in parallel.  
✅ **Efficient for I/O-bound tasks** – Best suited for network requests, database calls, and file operations.  
✅ **Not for CPU-bound tasks** – Since Python’s `asyncio` runs in a single thread, CPU-heavy tasks (like data processing) should use multiprocessing or threading instead.  

### Regular Functions Vs Coroutines?

Here’s a concise comparison highlighting the key differences between **coroutines** and **regular functions** in Python:

| Aspect                  | Regular Functions                       | Coroutines                                  |
|-------------------------|-----------------------------------------|--------------------------------------------|
| **Definition**          | Defined using the `def` keyword.       | Defined using the `async def` keyword.     |
| **Execution**           | Executes synchronously (one step at a time). | Executes asynchronously, allowing non-blocking concurrency. |
| **Return Type**         | Typically returns a value (e.g., `int`, `str`). | Returns a coroutine object, which needs to be awaited or run using an event loop. |
| **Calling**             | Directly callable. Example: `result = my_function()` | Needs `await` or an event loop. Example: `await my_coroutine()` or `asyncio.run(my_coroutine())` |
| **Concurrency**         | Blocks program execution until it completes. | Can pause its execution using `await` and yield control back to the event loop. |
| **Use Case**            | Used for standard, sequential operations. | Ideal for I/O-bound or time-consuming tasks (e.g., network requests, file handling). |

In essence, the major distinction is how they handle execution. Regular functions are straightforward and synchronous, while coroutines introduce asynchronous capabilities to enable efficient multitasking.

## **🔹 Difference Between `await` and `asyncio.run()`**  

| Feature                | `await`                 | `asyncio.run()` |
|------------------------|------------------------|------------------|
| **What it does?**      | Runs a **single coroutine** inside an async function | Runs an **entire async program** from sync code |
| **Where to use?**      | Inside an `async def` function | At the **top-level** in synchronous code |
| **Can be nested?**     | ✅ Yes, inside async functions | ❌ No, cannot be called inside another event loop |
| **Event loop needed?** | ✅ Yes, must be inside an event loop | ❌ No, creates and manages the event loop |
| **Use case?**         | When inside an async function and waiting for a coroutine to finish | Running an async function from the main script |

---

### **🚀 1️⃣ Using `await` (Inside an `async` Function)**
- `await` **pauses** execution until the coroutine completes.  
- You **must be inside an `async def` function** to use `await`.  

#### ✅ **Example: Using `await` Correctly**
```python
import asyncio

async def say_hello():
    await asyncio.sleep(2)  # Simulating an async task
    print("Hello, Async!")

async def main():
    await say_hello()  # ✅ Allowed because we are inside an async function

asyncio.run(main())  # Running the main function from sync code
```
✅ **Good** → `await` is used inside `main()`, which is an `async def` function.  

---

### **🛑 2️⃣ `await` CANNOT Be Used in Regular Code**
```python
import asyncio

async def say_hello():
    await asyncio.sleep(2)
    print("Hello, Async!")

# ❌ ERROR: 'await' outside an async function
await say_hello()
```
🛑 **Wrong!** `await` **must be inside an async function**.  

---

### **🔥 3️⃣ Using `asyncio.run()` (Top-Level Sync Code)**
- `asyncio.run()` **creates and runs an event loop**.  
- You **CANNOT call `await` at the top-level**, so `asyncio.run()` is needed in sync scripts.  

#### ✅ **Example: Using `asyncio.run()` Correctly**
```python
import asyncio

async def say_hello():
    await asyncio.sleep(2)
    print("Hello, Async!")

asyncio.run(say_hello())  # ✅ Runs the coroutine from sync code
```
✅ **Good** → Runs `say_hello()` from the main program.  

---

### **⚠️ 4️⃣ `asyncio.run()` CANNOT Be Called Inside an Existing Event Loop**
If you try to call `asyncio.run()` inside an already running async program (like in **Jupyter Notebook**), you'll get an error.

```python
import asyncio

async def task():
    print("Running inside an event loop")

asyncio.run(task())  # ❌ ERROR in Jupyter or nested async functions
```
🛑 **Wrong!** → `asyncio.run()` **cannot be called inside another event loop**.  

✅ **Fix:** Use `await` instead:
```python
await task()  # Works inside async functions or Jupyter Notebook
```

---

### **📌 When to Use What?**
| **Scenario**                    | **Use `await`?** | **Use `asyncio.run()`?** |
|----------------------------------|-----------------|--------------------|
| Inside an `async def` function  | ✅ Yes          | ❌ No |
| Running an async function from main script | ❌ No | ✅ Yes |
| Inside Jupyter Notebook or existing event loop | ✅ Yes | ❌ No (use `await`) |
| Running multiple coroutines in parallel | ✅ Yes | ❌ No |

---

### **🚀 TL;DR**
- Use **`await`** **inside** `async def` functions.  
- Use **`asyncio.run()`** **at the top-level** in sync code.  
- **Jupyter?** → Use `await`, NOT `asyncio.run()`.  

## asyncio.gather() ?

### **What Does `asyncio.gather()` Do?**  

`asyncio.gather()` is a function in Python’s `asyncio` module that runs multiple **coroutines concurrently** and waits for all of them to complete.  

### **How It Works**  
When you call:  
```python
await asyncio.gather(task1(), task2())
```
- Both `task1()` and `task2()` **start running at the same time**.
- The function **waits** for both tasks to finish before proceeding.
- It returns a list containing the results of all the coroutines.

---

### **Example: Running Two Coroutines Concurrently**
```python
import asyncio

async def task1():
    print("Task 1 started")
    await asyncio.sleep(2)
    print("Task 1 completed")
    return "Result 1"

async def task2():
    print("Task 2 started")
    await asyncio.sleep(1)
    print("Task 2 completed")
    return "Result 2"

async def main():
    results = await asyncio.gather(task1(), task2())
    print("All tasks completed:", results)

asyncio.run(main())
```
### **Expected Output:**
```
Task 1 started
Task 2 started
Task 2 completed
Task 1 completed
All tasks completed: ['Result 1', 'Result 2']
```
### **Why Use `gather()`?**
✅ **Runs coroutines concurrently** (better than `await` each one separately).  
✅ **Waits for all tasks to complete** before moving on.  
✅ **Returns all results in a list** (useful for processing multiple tasks).  

### When and When not to use gather().

**`asyncio.gather()` is used when you need to run multiple coroutines concurrently** and wait for all of them to complete.  

It is useful when:  
✅ You have **multiple independent coroutines** that should run at the same time.  
✅ You need to **collect results** from all the coroutines.  
✅ You want to **avoid blocking** while waiting for each coroutine separately.  

---

### **When NOT to Use `gather()`**
🚫 If you need **only one coroutine to run**, just use `await coroutine()`.  
🚫 If the tasks are **dependent on each other**, use `await` in sequence instead.  
🚫 If you want **fire-and-forget execution**, use `asyncio.create_task()` instead.  

## asyncio.create_task() ?

### See (Question set 5 (q5, q5_1, q5_2 to understand the difference clearly.))

### **`asyncio.create_task()` Explained**  

`asyncio.create_task()` is used to **schedule a coroutine as a separate background task**, allowing it to run **concurrently** with other tasks **without waiting** for it to complete immediately.  

Unlike `asyncio.gather()`, `create_task()` **does not wait for the task to finish**; it just starts it and moves on.

---

## **✅ Key Differences: `gather()` vs `create_task()`**
| Feature                | `asyncio.gather()`         | `asyncio.create_task()`  |
|------------------------|--------------------------|--------------------------|
| **Starts multiple coroutines?** | ✅ Yes | ✅ Yes |
| **Waits for all tasks to finish?** | ✅ Yes | ❌ No |
| **Returns results?** | ✅ Yes (list of results) | ❌ No (must `await` separately) |
| **Best for:** | Running multiple coroutines and collecting results | Running background tasks without waiting |

---

### **📝 Example: `asyncio.create_task()`**
```python
import asyncio

async def background_task():
    print("Background task started...")
    await asyncio.sleep(3)  # Simulate some async work
    print("Background task completed!")

async def main():
    print("Main function started")
    
    # Start background task but don't wait for it
    task = asyncio.create_task(background_task())

    print("Main function continues while background task runs...")
    await asyncio.sleep(1)
    print("Main function doing other work...")

    # Optionally wait for the background task before exiting
    await task  
    print("Main function completed")

asyncio.run(main())
```

### **🔹 Expected Output**
```
Main function started
Background task started...
Main function continues while background task runs...
Main function doing other work...
Background task completed!
Main function completed
```

---

## **🚀 When to Use `create_task()`**
✅ **Fire-and-forget** tasks that should run **in the background**.  
✅ When you **don’t need immediate results** from the coroutine.  
✅ Running a **continuous task** (e.g., monitoring, event listening) alongside other work.  

---

### **🛑 Common Mistake**
If you **don’t store the task in a variable**, it may get garbage collected before completion! ❌  
```python
asyncio.create_task(my_task())  # BAD: Task may not complete
```
✅ Always **keep a reference** to the task:  
```python
task = asyncio.create_task(my_task())  # GOOD
```