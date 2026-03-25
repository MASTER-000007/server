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

            # broadcast to all clients
            await asyncio.gather(
                *[client.send(message) for client in clients]
            )

    except Exception as e:
        print("❌ Error:", e)

    finally:
        print("🔌 Client disconnected")
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print("🚀 Server running...")
        await asyncio.Future()

asyncio.run(main())
