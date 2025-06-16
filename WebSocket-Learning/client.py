# client.py
import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello WebSocket!")
        response = await websocket.recv()
        print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(hello())
