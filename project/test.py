# coding=utf-8

import time
import sys
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
	with open(file, 'rb') as f:
		while True:
			try:
				b = f.read(1)       #可优化，想办法！
				if b == bytes([0x44]):
					b = f.read(3)
					if b == bytes([0x48, 0x41, 0x56]):
						bs = f.read(16)
						lists.append(create_dict(bs))
			except IOError:
				break
	lists = sorted(lists, key=cmp)
	return lists


def cmp(frame):
	return frame['number'].reverse()

def create_dict(b):  #这个通篇都是捉急，啊啊啊啊
	frame = {}
	bytess = [hex(x) for x in bytes(b)]
	frame['number'] = bytess[4:8]
	frame['size'] = bytess[8:12]
	frame['datetime'] = bytess[-4:]
	return frame


def write_file(lists):
	if not lists:
		return
	with open('done.txt', 'w') as f:
	    for i in lists:
	    	for key in i:
	    		f.write(key+':')
	    		i[key].reverse()
	    		f.write(''.join(i[key])+'\t')
	    f.write('\n')


'''文件位置：E:\dahua:TEST1'''
if __name__ == "__main__":
	start = time.time()

	file = sys.argv[1]
	lists = sort_frame(file)
	write_file(lists)

	end = time.time()
	print('这尼玛跑到多会了，操：', end-start)
