import threading
import time

def func_1(int_a=30):
    for i in range(int_a):
        print(f'thread_1 e func_1 exec idx {i}')
        time.sleep(0.5)

def func_2(int_b=30):
    for i in range(int_b):
        print(f'thread_2 e func_2 exec idx {i}')
        time.sleep(0.5)

thread_1 = threading.Thread(target=func_1)
thread_2 = threading.Thread(target=func_2)

thread_1.start()
thread_2.start()

for i in range(100):
    print(f'principal {i}')
    time.sleep(2)
thread_1.join()
thread_2.join()
