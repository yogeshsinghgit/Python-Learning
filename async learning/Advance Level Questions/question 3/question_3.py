# Intermediate API and DB Coroutine 
# Questions 3. 
# Fetch and Process Multiple API Calls Write a coroutine fetch_and_process() that: 
# Fetches user data from https://jsonplaceholder.typicode.com/users (or any public API). 
# Extracts the name and email of each user. Saves them into a PostgreSQL or SQLite database asynchronously.
# 👉 Bonus: Implement error handling for failed API calls.

# pip install aiohttp
# pip install asyncpg

import asyncio
import asyncpg
import aiohttp

async def fetch_user_data():
    """Fetch user data from the API asynchronously"""
    url = "https://jsonplaceholder.typicode.com/users"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print("User data fetch successfully!")
                    return data
                else:
                    print(f"Failed to fetch data. HTTP status: {response.status}")
    except aiohttp.ClientError as e:
        print(f"An error occured while fetching data: {e}")
        return None
    
    except Exception as e:
        print(f"Error {e}")
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