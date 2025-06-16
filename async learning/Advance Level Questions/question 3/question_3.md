Here's how you can implement the `fetch_and_process()` coroutine to fetch user data, process it to extract names and emails, and save it into a PostgreSQL database asynchronously using `asyncpg`. This includes error handling for API failures.

---

### Code Implementation

```python
import asyncio
import aiohttp
import asyncpg

async def fetch_user_data():
    """Fetch user data from the API asynchronously."""
    url = "https://jsonplaceholder.typicode.com/users"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:  # Check for successful response
                    data = await response.json()
                    print("User data fetched successfully!")
                    return data
                else:
                    print(f"Failed to fetch data. HTTP Status: {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"An error occurred while fetching data: {e}")
        return None

async def save_to_db(users, db_config):
    """Save the processed user data into a PostgreSQL database."""
    try:
        # Connect to the PostgreSQL database
        conn = await asyncpg.connect(**db_config)
        print("Connected to the database!")

        # Create the table if it doesn't exist
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

        # Insert user data
        for user in users:
            await conn.execute(
                "INSERT INTO users (name, email) VALUES ($1, $2)",
                user['name'], user['email']
            )
        print("User data saved to the database!")
    except Exception as e:
        print(f"An error occurred while saving to the database: {e}")
    finally:
        await conn.close()

async def fetch_and_process():
    """Fetch user data, process it, and save it into a PostgreSQL database."""
    db_config = {
        'user': 'your_username',
        'password': 'your_password',
        'database': 'your_database',
        'host': '127.0.0.1',
        'port': 5432
    }

    # Fetch data from the API
    user_data = await fetch_user_data()

    if user_data:
        # Extract name and email for each user
        users = [{'name': user['name'], 'email': user['email']} for user in user_data]
        print("Extracted user data:", users)

        # Save the extracted data to the database
        await save_to_db(users, db_config)

# Run the main coroutine
asyncio.run(fetch_and_process())
```

---

### Explanation:
1. **Fetching User Data (`fetch_user_data`)**:
   - Sends a GET request to the API using `aiohttp`.
   - Handles errors like network failures or non-200 HTTP responses using `try-except`.

2. **Processing Data**:
   - Extracts the `name` and `email` fields from the JSON response.

3. **Saving Data to the Database (`save_to_db`)**:
   - Uses `asyncpg` for interacting with PostgreSQL asynchronously.
   - Creates the `users` table if it doesn’t already exist.
   - Inserts the user data (`name` and `email`) into the table.

4. **Error Handling**:
   - Handles API fetch errors and database connection issues gracefully.

5. **Database Configuration**:
   - Replace the `db_config` dictionary fields (`user`, `password`, `database`, etc.) with your PostgreSQL connection details.

---

### Bonus: SQLite Alternative
If you prefer SQLite, replace `asyncpg` with `aiosqlite`. For example:
- Use `aiosqlite.connect()` to connect to the SQLite database.
- Use `CREATE TABLE` and `INSERT INTO` queries similarly.

---

### Dependencies:
To run this code, install the required libraries:
```bash
pip install aiohttp asyncpg
```

---

### Example Output:
```
User data fetched successfully!
Extracted user data: [{'name': 'Leanne Graham', 'email': 'Sincere@april.biz'}, ...]
Connected to the database!
User data saved to the database!
```

This implementation handles errors gracefully and works efficiently with asynchronous APIs and databases.