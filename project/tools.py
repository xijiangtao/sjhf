# coding=utf-8
'''写一些常用的函数'''
import binascii
from datetime import datetime
import re

def charArray_hex(array, base=16):
    '''把从大华光盘映像里读出来的字符串转换为正确的16进制'''
    array.reverse()
    tmp = '0x'
    for i in array:
        if len(i) == 3:
            tmp += '0'
        tmp += i[2:]
    tmp = int(tmp, base=base)
    return hex(tmp)


'''返回当前时间的正序16进制，用于筛选时段'''
def Time(year, month, day, hour, minute, seconds):
    pass


def sort_frame(array):
    sorted(array, key=lambda x:x['number'])


'''
text1 = text.encode('ascii')       字符串转换为ascii字节码
binascii.b2a_hex(text1)            以16进制形式表示
'''
