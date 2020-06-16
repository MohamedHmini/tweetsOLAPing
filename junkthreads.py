import concurrent.futures
import os
import time


def process(i):
    print(f"{i} starts")
    time.sleep(1)

def write(f,i):
    process(i)
    with open(os.path.abspath(f), 'a') as ff:
        for j in range(1000):
            ff.write(f"{j}")
        ff.write("\n")
    print(f"{i} finishes")
    return 0

with concurrent.futures.ThreadPoolExecutor(5) as ex:
    for i in range(100):
        ex.submit(lambda p: write(*p), ["./text.txt", i])


print('finish')
