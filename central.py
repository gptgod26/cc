import threading
import time

class Coordinator:
    def __init__(self):
        self.lock = threading.Lock()

    def request(self, pid):
        print(f"P{pid} requests Critical Section")

        self.lock.acquire()

        print(f"Coordinator grants permission to P{pid}")
        print(f"P{pid} ENTERS Critical Section")

        time.sleep(2)

        print(f"P{pid} LEAVES Critical Section")
        print(f"P{pid} sends RELEASE to Coordinator\n")

        self.lock.release()


def process(pid):
    coordinator.request(pid)


# Create coordinator
coordinator = Coordinator()

# Create 3 processes
threads = []

for i in range(3):
    t = threading.Thread(target=process, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
