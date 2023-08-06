from multiprocessing import Pool
from random import random
from time import sleep
import os

processed = 0

def f(x):
    sleep(random())
    global processed
    processed += 1
    print("Processed by %s: %s" % (os.getpid(), processed))
    return processed

if __name__ == '__main__':
    labels = ['zero', 'one', 'two', 'three']
    pool = Pool(processes=4)
    tasks = [pool.apply_async(f, args=(labels,))
             for r in range(10)]
    for t in tasks:
        print(t.get())

