import asyncio
import websockets
import os

PORT = int(os.environ.get("PORT", 10000))

clients = set()

async def handler(websocket, path):
    print("✅ Client connected")
    clients.add(websocket)

    try:
        async for message in websocket:
            print("📩 Received:", message)

            # send one by one (VERY IMPORTANT FIX)
            for client in list(clients):
                try:
                    await client.send(message)
                except:
                    clients.remove(client)

    except Exception as e:
        print("❌ Error:", e)

    finally:
        print("🔌 Client disconnected")
        clients.discard(websocket)

async def main():
    async with websockets.serve(
        handler,
        "0.0.0.0",
        PORT,
        ping_interval=None
    ):
        print("🚀 Server running...")
        await asyncio.Future()

asyncio.run(main())
