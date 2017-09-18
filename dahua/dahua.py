#!/usr/bin/env python
# coding=utf-8

import sqlite3
import struct
import mmap
import sys
import threading

from tools import *

lock = threading.Lock()

def write_img(file):
    lock.acquire()
    w.write(file)
    lock.release()

def insert(offset, number):
    lock.acquire()
    cursor.execute('INSERT INTO frames VALUES (%d, %d)' % (offset, number))
    lock.release()


if __name__ == '__main__':
    file = sys.argv[1]
    conn = sqlite3.connect('frame.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS frames(offset number, id inter primary key)')
    f = open(file, 'rb')
    w = open('dh.img', 'w+')
    m1 = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    flag = [bytes.fromhex('44484156'), bytes.fromhex('64686176')]
    ra = 0
    while 1:
        a = m1.find(flag[0], ra)
        if a!= -1:
            size, time = struct.unpack_from('2I', m1, a+12)  #把帧编号筛出来
            t = threading.Thread(target=insert, args=(a, number))
            t2 = threading.Thread(target=write_img, args=()) #把帧的数据拿出来，写进去
            ra = a+12   #文件指针挪动
        else:
            break
    print(num)
    conn.close()
