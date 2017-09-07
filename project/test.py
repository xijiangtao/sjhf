# coding=utf-8

import time
import sys

from hex_tools import charArray_hex
'''
解释如下：
0x00：4字节，数据帧的开始标志（大写的“DHAV”）。
0x04：2字节，帧类型（0xFD00表示关键帧，0xFC00表示非关键帧）。
0x06：2字节，通道号（从0开始计数）。
0x08：4字节，帧编号。
0x0C：4字节，帧大小，单位字节。
0x10：4字节，帧时间（Dtime）。
'''


def sort_frame(file):
    '''按照帧的编号排序帧'''
    lists = []
    f = [[0x48], [0x41], [0x56]]
    with open(file, 'rb') as f:
        while True:
            b = f.read(1)  
            if b == bytes([0x44]):
                b = f.read(1)
                if b == bytes([0x48]):
                    b = f.read(1)
                    if b == bytes([0x41]):
                        b = f.read(1)
                        if b == bytes([0x56]):
                            print('捕获成功')
                            print('实际读:', f.read(20))
                            bs = f.read(16)
                            print('bs:', bs)
                            lists.append(create_dict(bs))
    lists = sorted(lists, key=cmp)
    print(lists)
    return lists


def cmp(frame):
    return frame['number']


def create_dict(b):  # 这个通篇都是捉急，啊啊啊啊
    frame = {}
    bytess = [hex(x) for x in bytes(b)]
    print('bytess:', bytess)
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


'''文件位置：E:\dahua:TEST1'''
if __name__ == "__main__":
    start = time.time()
    print('开始')
    file = sys.argv[1]
    lists = sort_frame(file)
    write_file(lists)

    end = time.time()
    print('这尼玛跑到多会了，操：', end - start)
