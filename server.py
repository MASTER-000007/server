import socket
import threading

HOST = '0.0.0.0'
PORT = 10000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f"{username} left!".encode())
            usernames.remove(username)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("USERNAME".encode())
        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        broadcast(f"{username} joined!".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server running...")
receive()
