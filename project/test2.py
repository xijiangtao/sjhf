#coding=utf8

import sys
import asyncio

from db import *
from tools import *
import time


async def process(file):
    head = bytes.fromhex('44484156')
    end = bytes.fromhex('64686176')
    with open(file, 'rb') as f:
        while True:
            data = f.read(512)
            if not data:
                break
            index = data.find(head)
            if index != -1:
                if index + 20 >= 512:
                    new_data = data[index:] + f.read(20)
                else:
                    new_data = data[index:(index + 20)]
                new_data = [hex(x) for x in bytes(new_data)]
                await insert(f.tell()-512+index, int(charArray_hex(new_data[8:12]), 16))
                #if is_in_time(charArray_hex(new_data[-4:])):
    conn.commit()


if __name__ == '__main__':
    file = 'E:\TEST1.IMG'    #sys.argv[1]
    start = time.time()
    loop = asyncio.get_event_loop()
    task = process(file)
    loop.run_until_complete(task)
    end = time.time()
    print_frame()
    print('耗时：', end-start)
