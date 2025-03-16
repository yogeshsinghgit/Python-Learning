Here are some **real-world coroutine practice questions** involving **API calls and database operations** using `asyncio`, `aiohttp`, and `databases` (async DB library).  

---

### **Basic API and DB Coroutine Questions**  

#### **1. Fetch Data from an API Asynchronously**
Write a coroutine `fetch_data(url)` that:
- Uses `aiohttp` to send a `GET` request to the provided `url`.
- Waits for the response.
- Returns the response data as JSON.

👉 **Bonus:** Fetch data from **three different URLs concurrently** using `asyncio.gather()`.

---

#### **2. Save API Data to a Database**
Modify the `fetch_data(url)` coroutine to:
- Fetch data from an API.
- Store it in an **SQLite** database asynchronously using `databases` or `aiosqlite`.

👉 **Hint:** Use `asyncio.gather()` for batch inserts.

---

### **Intermediate API and DB Coroutine Questions**  

#### **3. Fetch and Process Multiple API Calls**
Write a coroutine `fetch_and_process()` that:
- Fetches user data from `https://jsonplaceholder.typicode.com/users` (or any public API).
- Extracts the name and email of each user.
- Saves them into a **PostgreSQL** or **SQLite** database asynchronously.

👉 **Bonus:** Implement **error handling** for failed API calls.

---

#### **4. Rate-Limiting API Requests**
Modify your API fetch function to:
- Limit the number of simultaneous API calls to **5** using `asyncio.Semaphore()`.

👉 **Hint:** Use:
```python
semaphore = asyncio.Semaphore(5)
```

---

#### **5. Concurrent Database Queries**
Write an async function that:
- Connects to a **PostgreSQL** or **MySQL** database.
- Executes **multiple SELECT queries concurrently**.
- Uses `asyncio.gather()` to run them in parallel.

👉 **Bonus:** Fetch **orders and users** from two tables at the same time.

---

### **Advanced API and DB Coroutine Questions**  

#### **6. Paginated API Requests**
Some APIs return paginated results. Write a coroutine `fetch_all_pages()` that:
- Fetches **all pages** of data from an API (e.g., GitHub, Twitter).
- Combines the results into a single list.

👉 **Hint:** Extract the next page URL from API responses.

---

#### **7. Handling API Timeouts and Retries**
Modify your API fetch function to:
- **Retry** failed requests up to 3 times.
- **Timeout** requests if they take longer than **2 seconds**.

👉 **Hint:** Use `asyncio.wait_for()` and `aiohttp.ClientSession()`.

---

#### **8. Async Producer-Consumer for API and DB**
Build an **async producer-consumer** system:
- **Producer**: Fetches data from an API and pushes it into an `asyncio.Queue`.
- **Consumer**: Reads from the queue and **saves the data** into a database.

👉 **Hint:** Use `asyncio.Queue()`.

---

#### **9. Parallel API Calls with Batching**
Modify your API fetch function to:
- Fetch **1000 users** from an API.
- Process them in **batches of 50** using `asyncio.gather()`.

👉 **Hint:** Use:
```python
for i in range(0, len(urls), 50):
    batch = urls[i : i + 50]
    results = await asyncio.gather(*[fetch_data(url) for url in batch])
```

---

#### **10. Async API Data Sync to Database**
Write an **ETL (Extract, Transform, Load)** pipeline:
1. **Extract:** Fetch data from an API.
2. **Transform:** Clean and filter the data.
3. **Load:** Insert it into a PostgreSQL/MySQL database **asynchronously**.

👉 **Bonus:** Implement **logging and error handling**.

---
