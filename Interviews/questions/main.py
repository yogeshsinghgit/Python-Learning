# def add_item(item, items=[]):
#     items.append(item)
#     return items

# print(add_item(1)) 
# print(add_item(2))
# # [1, 2] 
# # 

import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "data"

async def main():
    results = []
    for i in range(3):
        result = await fetch_data()  
        results.append(result)
        
    print(results)

asyncio.run(main())