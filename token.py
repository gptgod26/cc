import threading
import time

n = 3
token = 0
lock = threading.Lock()

def process(pid):
    global token

    for _ in range(1):
        # Wait until this process gets the token
        while True:
            with lock:
                if token == pid:
                    break
            time.sleep(0.1)

        print(f"P{pid} receives TOKEN")
        print(f"P{pid} ENTERS Critical Section")
        time.sleep(1)
        print(f"P{pid} LEAVES Critical Section")

        # Pass token to the next process in the ring
        with lock:
            token = (pid + 1) % n

        print(f"P{pid} passes TOKEN to P{token}\n")


threads = []

for i in range(n):
    t = threading.Thread(target=process, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
