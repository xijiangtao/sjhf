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
        omit = f.read(3)
        while True:
            b = f.read(510)
            if not b:
                break
            data = omit + b
            omit = b[-3:]
            index = data.find(head)
            if index != -1:
                if index + 16 >= 512:
                    tmp = 20 - 512 + index  #获取缺少的部分
                    new_data = data[index:] + f.read(tmp)
                    index -= tmp
                else:
                    new_data = data[index:(index + 20)]
                new_data = [hex(x) for x in bytes(new_data)]
                number = charArray_hex(new_data[8:12])
                await insert(f.tell()-512+index, number)
                if is_in_time(charArray_hex(new_data[-4:])):
                    with open('frames/{}'.format(number), 'w') as w:
                        while True:
                            write = f.read(512)
                            if not write:
                                break
                            i2 = write.find(end)
                            if i2 != -1:
                                w.write(write[:i2])
                                f.seek(f.tell()-(512-i2))
                                break
                            else:
                                w.write(write)
    conn.commit()


if __name__ == '__main__':
    file = sys.argv[1]

    start = time.time()

    loop = asyncio.get_event_loop()
    task = process(file)
    loop.run_until_complete(task)
    loop.close()

    end = time.time()
    print('耗时：', end-start, 's')
