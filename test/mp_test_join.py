from multiprocessing import Process
import time

def work():
    print("子进程开始工作")
    time.sleep(2)
    print("子进程完成")

p = Process(target=work)
p.start()
print("主进程等待子进程结束")
# 注释掉下面的代码行 或者 使用 p.join() 来等待子进程结束
p.join()
print("主进程继续运行")
