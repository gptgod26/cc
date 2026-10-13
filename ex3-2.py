import threading
import time

n = 3
cs_lock = threading.Lock()
clock = 0
clock_lock = threading.Lock()

def process(pid):
    global clock
    with clock_lock:
        clock+=1
        timestamp = clock

    print(f'P{pid} sends request with timestamp {timestamp}')

    replies = 0

    for other in range(1, n + 1):

        if other != pid:
            with clock_lock:
                clock+=1

            time.sleep(0.5)
            print(f'P{pid} receives reply from P{other}')
            replies += 1
        

    if replies == n - 1:
        clock+=1
        with cs_lock:
            with clock_lock:
                clock+=1
                
            print(f'P{pid} enters CS')
            time.sleep(1)
            print(f'P{pid} leaves CS')

threads = []
clock = 0

for i in range(1, n + 1):
    t = threading.Thread(target=process, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
