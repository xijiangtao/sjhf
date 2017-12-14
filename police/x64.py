# coding=utf-8

import struct
import mmap
import os
import sys


def memory_map(filename, access=mmap.ACCESS_READ):
    size = os.path.getsize(filename)
    fd = open(filename, "rb")
    return mmap.mmap(fd.fileno(), size, access=access)


def process(keyframe, hdvr, non_key):
    channel = struct.pack('B', keyframe[2])  # 本帧的通道号
    frame_end, = struct.unpack('<i', keyframe[4:8])  # 本帧的结束
    content = b'\x10' + keyframe[1:3] + b'\x00' + keyframe[4:] + hdvr.read(frame_end)  # 关键帧
    for _ in range(49):
        non_offset = hdvr.find(b'\x80\x00' + channel + b'\x01')
        if non_offset not in non_key and hdvr[non_offset + 16:non_offset + 20] == b'\x00\x00\x01\xB6':
            non_key.add(non_offset)
        else:
            break
        hdvr.seek(non_offset)
        head = hdvr.read(16)
        size, = struct.unpack('<I', head[4:8])
        content += b'\x90' + head[1:3] + b'\x00' + head[4:] + hdvr.read(size)  # 非关键帧
    return content

'''
find all frame. sort frame head, write dvr file.
'''

def main(file):
    hdvr = memory_map(file)
    packer_head = b'\x00\x02\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\xd0\x02\x00\x00\x00\x00\x00\x00' \
                    b'\x76\x45\x9D\x06\xD2\x04\x00\x00\x14\xFC\x01\x00'
    head = [packer_head for _ in range(255)]    
    num = [0 for _ in range(255)]
    non_key = set()
    key_flag = 0
    c = set()
    while 1:
        key = b'\x00\x00\x01\xB6'
        offset = hdvr.find(key, key_flag)
        if offset == -1:
            while c:
                channel = c.pop()
                with open('channel-%s-%d.dvr' % (channel, num[channel]), 'rb+') as f:
                    f.write(head[channel])
            break
        key_flag = offset + 1
        if offset and hdvr[offset-16:offset-14] == b'\x00\x00' and hdvr[offset-13] == 1:
            hdvr.seek(offset)
            keyframe = hdvr[offset-16:offset]
            channel = keyframe[2]
            c.add(int(channel))
            dvr_file = 'channel-%s-%d.dvr' % (channel, num[channel])
            try:
                size = os.path.getsize(dvr_file)
                f = open(dvr_file, 'ab')
            except FileNotFoundError:
                f = open(dvr_file, 'wb')
                f.seek(128028)
            f.write(process(keyframe, hdvr, non_key))
            try:
                head[channel] += b'\xA8\x62\x00\x00' + struct.pack('<I', f.tell())
            except struct.error:
                f.close()
                with open(file, 'rb+') as f:
                    f.seek(0)
                    f.write(head[channel])
                    print('生成文件：', file)
                head[channel] = packer_head
                num[channel] += 1
            f.close()


if __name__ == '__main__':
    print('视频文件将在本exe目录下生成')
    file = input('请输入包含文件绝对路径的文件名：')
    main(file)
    print('整理完毕')
    a = input(' ')