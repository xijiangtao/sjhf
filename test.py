#!/usr/bin/env python
# coding=utf-8

import threading
import multiprocessing
import sys
import time

def process(lock, f):
    while True:
        with lock:
            try:
                content = f.read(20)
                if content == None or len(content) == 0:
                    break
                print(content)
            except:
                break

if __name__ == '__main__':
    file = sys.argv[1]
    lock = threading.Lock()
    f = open(file, 'r')
    start = time.time()
    for _ in range(4):
        t = threading.Thread(target=process, args=(lock, f))
        t.start()
        t.join()
    end = time.time()
    print(end-start)
    f.close()
