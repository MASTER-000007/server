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

            # broadcast to all clients safely
            await asyncio.gather(
                *[client.send(message) for client in clients if client.open],
                return_exceptions=True
            )

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
        ping_interval=None,   # 🔥 DISABLE ping timeout
    ):
        print("🚀 Server running...")
        await asyncio.Future()

asyncio.run(main())
