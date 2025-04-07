import multiprocessing as mp
import time
from datetime import datetime
import os
def timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def worker1(name):
    print(f"[{timestamp()}][启动] 当前进程: {mp.current_process().name},PID: {os.getpid()}")
    # time.sleep(1)
    print(f"[{timestamp()}] {name} process done")

def worker2(name):
    print(f"[{timestamp()}][启动] 当前进程: {mp.current_process().name},PID: {os.getpid()}")
    # time.sleep(1)
    print(f"[{timestamp()}] {name} process done")

if __name__ == '__main__':
    print(f"[{timestamp()}][启动] 当前进程: {mp.current_process().name},PID: {os.getpid()}")
    p = mp.Process(target=worker1, args=("work1",))
    p.start()

    q = mp.Process(target=worker2, args=("work2",))
    q.start()

    print(f"[{timestamp()}] Main process Done")

