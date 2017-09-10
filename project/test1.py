# coding=utf-8

import time
import sys
import asyncio

from tools import charArray_hex
'''
大华和海康的要求：
    根据帧编号进行排序
    提取 8.10 到 当前时间每天 7：00~8：30     17：00~18：30
'''



async def sort_frame(file):
    '''按照帧的编号排序帧'''
    lists = []
    head = [bytes([0x44]), bytes([0x48]), bytes([0x41]), bytes([0x56])]
    with open(file, 'rb') as f:
        index = 0
        while True:
            b = f.read(1)
            if not b:
                break
            if b != head[index]:
                index = 0
                continue
            else:
                index += 1
            if index == 4:
                index = 0
                bs = f.read(16)
                number, flag = process(bs)
                lists.append(number)
    sorted(lists)
    await write_file(lists)
    return lists



def process(b):  
    b = [hex(x) for x in bytes(b)]
    '''
    判断是否在时间范围内
    if charArray_hex(bytes[-4:]) < ?:
        flag = True
    else:
        flag = False
    '''

    return (charArray_hex(b[4:8]), 1)

'''
def write_file(lists):
    if not lists:
        return
    with open('done.txt', 'w') as f:
        for i in lists:
            for key in i:
                f.write(key + ':')
                f.write(''.join(i[key]) + '\t')
            f.write('\n')
'''
async def write_file(list):
    with open('sort.txt', 'w') as f:
        for i in list:
            await f.write('serial number:' + i)


if __name__ == "__main__":
    file = sys.argv[1]
    start = time.time()

    loop = asyncio.get_event_loop()
    task = sort_frame(file)
    loop.run_until_complete(task)

    end = time.time()
    print('耗费时间：', end-start)
