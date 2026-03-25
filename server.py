import asyncio
import websockets
import os

PORT = int(os.environ.get("PORT", 10000))

clients = {}
# websocket → username

async def broadcast_users():
    users = ",".join(clients.values())
    message = f"__USERS__:{users}"
    for client in clients:
        await client.send(message)

async def handler(websocket, path):
    print("✅ Client connected")

    try:
        # first message = username
        username = await websocket.recv()
        clients[websocket] = username

        print(f"👤 {username} joined")

        await broadcast_users()

        async for message in websocket:
            print("📩", message)

            for client in clients:
                await client.send(message)

    except:
        pass

    finally:
        username = clients.get(websocket, "Unknown")
        print(f"🔌 {username} disconnected")

        if websocket in clients:
            del clients[websocket]

        await broadcast_users()

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
