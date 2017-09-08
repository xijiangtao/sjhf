# coding=utf-8

import time
import sys
import asyncio

from hex_tools import charArray_hex
'''
大华和海康的要求：
    根据帧编号进行排序
    提取 8.10 到 当前时间每天 7：00~8：30     17：00~18：30
'''

#把处理程序改成异步。
def process(file):
    '''按照帧的编号排序帧'''
    lists = []
    return lists

def sort_frame(lists):    #外部归并排序
    pass


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
    while True:
        lists = process(file)
        write_file(lists)