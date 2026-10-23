import socket
import time

client = socket.socket()
client.connect(("127.0.0.1", 5000))

pid = int(input("Enter Process ID : "))

print(f"Process {pid} requesting Critical Section")

client.send("REQUEST".encode())

response = client.recv(1024).decode()
if response == "GRANTED":
    print(f"Process {pid} permitted to enter critical section")
    time.sleep(5)
    print(f"Process {pid} exiting critical section")
    client.send("RELEASE".encode())

client.close()
