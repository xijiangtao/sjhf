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
        tmp += i[2:]
    tmp = int(tmp, base=base)
    return hex(tmp)


'''返回当前时间的16进制，用于筛选时段'''
def now():
	now_time = datetime.now()
	c = str(now_time)[2:-7]
	result = ''
	for i in c:
		t = ord(i)
		if t > 47 and t < 58:
			result += i
	return hex(int(result))


def sort_frame(array):
    sorted(array, key=lambda x:x['number'])
'''
text1 = text.encode('ascii')       字符串转换为ascii字节码
binascii.b2a_hex(text1)            以16进制形式表示
'''
