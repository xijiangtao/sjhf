#! /usr/bin/dev python3 
#coding=utf8


#py3.5版本的异步读写
import asyncio
import os
import fcntl                 # 原本是unix系统调用 fcntl
import sys

class asyncFile():
	BLOCK_SIZE = 512

	def __init__(self, filename, mode, loop=None):
		self.fd = open(filename, mode=mode)  #打开文件对象
		flag = fcntl.fcntl(self.fd, fcntl.F_GETFL)  #把文件对象fd设置成非阻塞的
		if fcntl.fcntl(self.fd, fcntl.F_SETFL, flag|os.O_NONBLOCK) != 0:
			raise OSError()

		if loop is None:
			loop = asyncio.get_event_loop()
		self.loop = loop
		self.rbuffer = bytearray()   #返回长度为0的字节数组

	def read_step(self, future, n, total):
		res = self.fd.read(n)

		if res is None:
			'''第一个参数是回调函数，让回调参数尽快被调用，当控制权回来时，如果
			上一个call_soon已经返回，则开始调用下一个回调参数。类似于队列。
			'''
			self.loop.call_soon(self.read_step, future, n, total)
			return

		if not res:     #EOF
			future.set_result(bytes(self.rbuffer)) #标记未来完成并设置结果。
			return 
		self.rbuffer.extend(res)  #res加入到rbuffer

		if total > 0:
			left = total - len(self.rbuffer)
			if left <= 0:
				future.set_result(bytes(self.rbuffer))
			else:
				left = min(self.BLOCK_SIZE, left)
				self.loop.call_soon(self.read_step, future, left, total)
		else:
			self.loop.call_soon(self.read_step, future, self.BLOCK_SIZE, total)

	def read(self, n=-1):
		future = asyncio.Future(loop=self.loop)

		if n == 0:
			future.set_result(b'')
			return future          #return none对应的是not res
		elif n < 0:
			self.rbuffer.clear()
			self.loop.call_soon(self.read_step, future, self.BLOCK_SIZE, n)
		else:
			self.rbuffer.clear()
			self.loop.call_soon(self.read_setup, future, min(self.BLOCK_SIZE, n), n)

		return future


async def test(file):
	af = asyncFile(file, mode='rb')
	content = await af.read(512)
	print(content)

if __name__ == '__main__':
	file = sys.argv[1]
	import time
	start = time.time()
	task = [test(file)]
	asyncio.get_event_loop().run_until_complete(asyncio.wait(task))
	end = time.time()
	print('耗时：', end-start)