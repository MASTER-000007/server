import socket
import threading
import os

HOST = '0.0.0.0'
PORT = int(os.environ.get("PORT", 10000))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

print("🚀 Server running...")

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        username = usernames[index]
        usernames.remove(username)
        broadcast(f"{username} left the chat!".encode())
        client.close()

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                remove_client(client)
                break
            broadcast(message)
        except:
            remove_client(client)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"✅ Connected with {address}")

        try:
            client.send("USERNAME".encode())
            username = client.recv(1024).decode()

            if not username:
                client.close()
                continue

            usernames.append(username)
            clients.append(client)

            print(f"👤 {username} joined")
            broadcast(f"👤 {username} joined the chat!".encode())

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

        except:
            client.close()

receive()
