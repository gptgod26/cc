import time

class Process:
    def __init__(self,pid,n):
        self.pid=pid
        self.n=n
        self.clock=0
        self.reply_count=0
        self.requesting=False
        self.request_time=0
        self.deferred=[]

    def request_cs(self):
        self.clock+=1
        self.request_time=self.clock
        self.requesting=True
        self.reply_count=0

        print(f"{self.pid} trying to enter cs")

        for i in range(self.n):
            if i!=self.pid:
                processes[i].receive_request(self.pid,self.request_time)

        while self.reply_count < self.n - 1:
            time.sleep(0.1)

        self.enter_cs()

    def receive_request(self,sender_id,sender_timestamp):
        self.clock=max(self.clock,sender_timestamp)+1

        if not self.requesting:
            processes[sender_id].receive_reply(self.pid)

        elif sender_timestamp < self.request_time:
            processes[sender_id].receive_reply(self.pid)

        else:
            self.deferred.append(processes[sender_id])

    def receive_reply(self,receiver_pid):
        self.reply_count+=1
        print(f"{receiver_pid} allowed to enter cs")

    def enter_cs(self):
        print(f"{self.pid} entering the cs")
        time.sleep(1)
        print(f"{self.pid} leaving the cs")

        self.requesting=False

        for i in self.deferred:
            self.receive_request(i.pid,i.request_time)
        self.deferred.clear()


n=3

processes=[Process(i,n) for i in range(n)]

processes[0].request_cs()
