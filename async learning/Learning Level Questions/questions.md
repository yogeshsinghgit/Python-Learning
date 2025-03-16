Here are some **coding questions on coroutines** to test and enhance your understanding:

---

### **Basic Level**
1. **Define a coroutine**  
   Write a coroutine named `hello_coroutine` that prints `"Hello, Async!"`, waits for 2 seconds, and then prints `"Coroutine Finished"`.

2. **Run a coroutine**  
   How do you run a coroutine named `my_coroutine()` in Python?

3. **Awaiting a coroutine**  
   What happens if you try to call a coroutine using `my_coroutine()` without `await` or `asyncio.run()`?

4. **Multiple coroutines execution**  
   Write an `async` function that runs two coroutines (`task1()` and `task2()`) **concurrently** using `asyncio.gather()`.

---

### **Intermediate Level**
5. **Simulating an I/O-bound task**  
   Write a coroutine `fetch_data()` that simulates fetching data from a server by waiting for 3 seconds (`await asyncio.sleep(3)`) and then returning `"Data received"`.

6. **Handling coroutines with timeouts**  
   Modify the `fetch_data()` coroutine to raise a `TimeoutError` if it takes longer than 2 seconds using `asyncio.wait_for()`.

7. **Task cancellation**  
   Write a coroutine that starts a long-running task (`asyncio.sleep(5)`) but cancels it after 2 seconds.

---

### **Advanced Level**
8. **Using an event loop manually**  
   Without using `asyncio.run()`, start an event loop and run the `fetch_data()` coroutine inside it.

9. **Implement a producer-consumer pattern**  
   Use `asyncio.Queue` to implement a producer-consumer system where the producer generates numbers every second, and the consumer processes them.

10. **Rate-limiting coroutines**  
    Write an `async` function that ensures only **3 tasks** run concurrently using `asyncio.Semaphore()`.

---
