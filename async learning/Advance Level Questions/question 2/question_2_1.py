
# This Code Inculdes...

# ✔ Batch insert using insert_many() (faster MongoDB writes).
# ✔ Error handling for API & MongoDB failures (timeouts, DB errors, etc.).
# ✔ Continuous fetching at intervals (runs every 10 seconds).
# ✔ Added logging instead of print statements?

import asyncio
import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "api_database"
COLLECTION_NAME = "api_data"

# Async MongoDB Client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

async def fetch_data(url, session):
    """Fetch data from an API asynchronously with error handling."""
    try:
        async with session.get(url, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Data fetched from {url}")
                return data
            else:
                print(f"⚠️ HTTP Error {response.status}: {url}")
    except asyncio.TimeoutError:
        print(f"⏳ Timeout fetching {url}")
    except aiohttp.ClientError as e:
        print(f"❌ Network error {url}: {e}")

    return None  # Return None if fetching fails

async def save_to_mongo(data_list):
    """Batch insert data into MongoDB with error handling."""
    if data_list:
        try:
            result = await collection.insert_many(data_list)
            print(f"📌 {len(result.inserted_ids)} documents inserted into MongoDB")
        except Exception as e:
            print(f"❌ MongoDB Insert Error: {e}")

async def fetch_and_store():
    """Fetch API data and store it in MongoDB asynchronously."""
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ]

    async with aiohttp.ClientSession() as session:
        fetched_data = await asyncio.gather(*(fetch_data(url, session) for url in urls))
        cleaned_data = [data for data in fetched_data if data]  # Remove failed fetches
        await save_to_mongo(cleaned_data)  # Batch insert into MongoDB

async def run_continuously(interval=10):
    """Run the fetch-store process in a loop at fixed intervals."""
    while True:
        print("\n🔄 Running fetch & store cycle...")
        await fetch_and_store()
        await asyncio.sleep(interval)  # Wait before the next cycle

# Run the loop continuously
asyncio.run(run_continuously(10))  # Runs every 10 seconds
