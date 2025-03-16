
# 2. Save API Data to a Database
# Modify the fetch_data(url) coroutine to:

# Fetch data from an API.
# Store it in an SQLite database asynchronously using databases or aiosqlite.
# 👉 Hint: Use asyncio.gather() for batch inserts.
# Use mongodb localhost for database.

import aiohttp
import asyncio 
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Config
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "api_database"
COLLECTION_NAME = "api_data"


# Initialize MongoDB Client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


async def fetch_data(url):
    """Fetch data from the provided URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()  # Fetch response as JSON
                print(f"Data fetched from {url}")
                return data
            else:
                print(f"Error {response.status}: {url}")
                return None
        
async def save_to_mongo(data):
    """Save fetched data to MongoDB asynchronously."""
    if data:
        result = await collection.insert_one(data)
        print(f"📌 Data saved with ID: {result.inserted_id}")


async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ]

    # Fetch data concurrently
    fetched_data = await asyncio.gather(*(fetch_data(url) for url in urls))

    # Insert only non-empty data into MongoDB
    await asyncio.gather(*(save_to_mongo(data) for data in fetched_data if data))

asyncio.run(main())  # Run the async event loop  