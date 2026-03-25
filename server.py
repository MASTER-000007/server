import asyncio
import websockets
import os

PORT = int(os.environ.get("PORT", 10000))

clients = set()

async def handler(websocket, path):
    print("✅ New client connected")
    clients.add(websocket)
    try:
        async for message in websocket:
            print("Received:", message)
            for client in clients:
                await client.send(message)   # send to ALL (including sender)
    except:
        print("Client disconnected")
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print("🚀 Server running...")
        await asyncio.Future()

asyncio.run(main())
