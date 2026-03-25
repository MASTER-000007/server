import asyncio
import websockets
import os

PORT = int(os.environ.get("PORT", 10000))

clients = set()

async def handler(websocket):
    print("✅ Client connected")
    clients.add(websocket)

    try:
        async for message in websocket:
            print("📩 Received:", message)

            # broadcast safely
            dead_clients = []
            for client in clients:
                try:
                    await client.send(message)
                except:
                    dead_clients.append(client)

            # remove dead clients
            for dc in dead_clients:
                clients.remove(dc)

    except Exception as e:
        print("❌ Error:", e)

    finally:
        print("🔌 Client disconnected")
        if websocket in clients:
            clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print("🚀 Server running...")
        await asyncio.Future()

asyncio.run(main())
