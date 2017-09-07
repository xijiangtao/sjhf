# coding=utf-8
'''写一些常用的函数'''
import binascii


def charArray_hex(array, base=16):
    '''把从大华光盘映像里的文件读出数值来'''
    array.reverse()
    tmp = '0x'
    for i in array:
        tmp += i[2:]
    print(tmp)
    tmp = int(tmp, base=base)
    return hex(tmp)


'''
text1 = text.encode('ascii')       转换为ascii字节码
binascii.b2a_hex(text1)            以16进制形式表示
'''
