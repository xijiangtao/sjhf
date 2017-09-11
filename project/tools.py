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


start_date = '010001100001010'
end_date = '010001100101011'       #9.11

t1_start = '00111000000000000'      #7点到8点半
t1_end = '01000010100000000'

t2_start = '10001000000000000'        #17点到18点半
t2_end = '10010010100000000'
def is_in_time(s):   #判断是否在指定时间范围内
    t = bin(int(s, 16))   #从2到18表示年月日，剩下的表示具体时间
    if t[2:-17] > start_date and t[2:17] < end_date:
        if t1_start < t[-17:] < t1_end or  t2_start < t[-17:] < t2_end:
            return True



'''
text1 = text.encode('ascii')       字符串转换为ascii字节码
binascii.b2a_hex(text1)            以16进制形式表示
'''
