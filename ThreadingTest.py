import threading
import time

thisList = []


def function1(this=None):
    time.sleep(2)
    thisList.append(1)
    print("func 1 done", this)


def function2():
    time.sleep(5)
    thisList.append(2)
    print("func 2 done")


thread1 = threading.Thread(target=function1)
thread2 = threading.Thread(target=function2)
thread1.setDaemon = True

print("started")
thread1.start()
thread2.start()

thread1.join()
print(thisList)
print("main done")
