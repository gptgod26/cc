import socket
import threading

server = socket.socket()
server.bind(("127.0.0.1", 5000))
server.listen()

lock = threading.Lock()


def handle_client(client, addr):
    print(f"Client Connected from {addr}")

    while True:
        msg = client.recv(1024).decode()

        if not msg:
            break

        if msg == "REQUEST":
            print(f"{addr} requested Critical Section")

            lock.acquire()
            client.send("GRANTED".encode())
            print(f"{addr} entered Critical Section")

        elif msg == "RELEASE":
            lock.release()

            print(f"{addr} exited the Critical Section")

    client.close()


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_client, args=[client, addr], daemon=True).start()
import socket
import threading

server = socket.socket()
server.bind(("127.0.0.1", 5000))
server.listen()

lock = threading.Lock()


def handle_client(client, addr):
    print(f"Client Connected from {addr}")

    while True:
        msg = client.recv(1024).decode()

        if not msg:
            break

        if msg == "REQUEST":
            print(f"{addr} requested Critical Section")

            lock.acquire()
            client.send("GRANTED".encode())
            print(f"{addr} entered Critical Section")

        elif msg == "RELEASE":
            lock.release()

            print(f"{addr} exited the Critical Section")

    client.close()


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_client, args=[client, addr], daemon=True).start()
