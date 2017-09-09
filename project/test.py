# coding=utf-8

import time
import sys
import asyncio

from tools import charArray_hex, sort_frame
'''
大华和海康的要求：
    根据帧编号进行排序
    提取 8.10 到 当前时间每天 7：00~8：30     17：00~18：30
'''


def process(file):
    '''按照帧的编号排序帧'''
    lists = []
    head = [bytes([0x44]), bytes([0x48]), bytes([0x41]), bytes([0x56])]
    with open(file, 'rb') as f:
        index = 0
        num = 0
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
                lists.append(create_dict(bs))
                num += 1
            if num == 1000:
                break
    sort_frame(lists)
    return lists



def create_dict(b):  # 通篇都是捉急
    frame = {}
    bytess = [hex(x) for x in bytes(b)]
    frame['number'] = charArray_hex(bytess[4:8])
    frame['size'] = charArray_hex(bytess[8:12])
    frame['datetime'] = charArray_hex(bytess[-4:])
    return frame


def write_file(lists):
    if not lists:
        return
    with open('done.txt', 'w') as f:
        for i in lists:
            for key in i:
                f.write(key + ':')
                f.write(''.join(i[key]) + '\t')
            f.write('\n')



if __name__ == "__main__":
    file = sys.argv[1]
    lists = process(file)
    write_file(lists)
