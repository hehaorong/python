# -*- coding:utf8 -*-
# !/usr/bin/env python3

import sys
import struct
import collections

# import collections.Iterable

__doc__ = "协议包解析工具类"


class ByteArray(object):
    """"字节数组, 本类封装协议包的多字节数据、多字节整形数据填充填充与获取.
        packet = ByteArray()
        txpacket.writebytes(0x48).writebytes(0x01).writebytes(0x00).writebytes(0x49)
        serial.send(txpacket.packet)

        rxpacket = ByteArray(packet)
        rxpacket.readbyte()
        rxpacket.readbyte()
        rxpacket.readbyte()
    """

    def __init__(self, packet=None):
        self._byteorder = sys.byteorder
        self.pkgsize = 0
        self.packet = bytearray(packet if packet else [])

    def __str__(self):
        """方便输出数据字节"""
        return ''.join(["%02x " % e for e in self.packet])
     
    # def __getitem__(self, item):
    #     """返回协议包第idx个元"""
    #     if item < len(self.packet):
    #         return self.packet[item]
    #     else:
    #         raise IndexError("index > len(self.packet)")

    def __setitem__(self, idx, value):
        """给协议包第idx个位置设置元"""
        if (idx == len(self.packet)):
            self.writebytes(value)
        else:
            self.packet[idx] = value

    def __len__(self):
        """返回协议包长度"""
        return len(self.packet)

    def writebytes(self, data):
        """向字节数组写入单个或多个字节数数据, data-> int, bytes, str"""

        # 对应数据为字符串则进行UTF-8编码
        data = data.encode("UTF-8") if isinstance(data, str) else data
        if isinstance(data, collections.Iterable):
            self.packet.extend(data)  # 多个字节数据使用extend方法插入
        else:
            self.packet.append(data)  # 单字节数据使用append插入
        return self

    def _writemultibytes(self, data, fmt):
        """向字节数组写入大端格式的多字节整型数据"""
        self.packet.extend(struct.pack('!%c' % fmt, data))
        return self

    def write2byte(self, data):
        """"向字节数组写入大端格式的uint16_t整型数据"""
        return self._writemultibytes(data, 'H')

    def write4byte(self, data):
        """向字节数组写入大端格式的uint32_t整型数据"""
        return self._writemultibytes(data, 'I')

    def write8byte(self, data):
        """向字节数组写入大端格式的uint64_t整型数据"""
        return self._writemultibytes(data, 'Q')

    def readbyte(self, idx=0):
        """从协议包(字节数组)中读取单字节数据"""
        data = self.packet[idx] if len(self.packet) > idx else None
        return data

    def readbytes(self, idx=0, cnt=0):
        """从协议包(字节数组)中读取多字节数据"""
        data = None
        # byte_cnt=0表示读取所有字节, 指定字节数比数组的剩余字节数长则读取剩余字节
        if 0 == cnt or idx + cnt > len(self.packet):
            data = self.packet[idx:] if len(self.packet) > idx else []
        else:
            data = self.packet[idx: idx + cnt]
        return data

    def _readmultibytes(self, idx=0, fmt='B'):
        """从协议包(字节数组)中读取多字节整型数据并转换成本地字节序"""
        data = None
        size = struct.calcsize(fmt)
        if idx + size < len(self.packet):
            data = struct.unpack("!%c" % fmt, self.packet[idx:idx + size])
        return data

    def read2byte(self, idx=0, fmt='H'):
        """从协议包(字节数组)中读取uint16_t整型数据并转换成本地字节序"""
        return self._readmultibytes(idx, fmt)

    def read4byte(self, idx=0, fmt='I'):
        """从协议包(字节数组)中读取uint32_t整型数据并转换成本地字节序"""
        return self._readmultibytes(idx, fmt)

    def read8byte(self, idx=0, fmt='Q'):
        """从协议包(字节数组)中读取uint64_t整型数据并转换成本地字节序"""
        return self._readmultibytes(idx, fmt)

    def append(self, data):
        """将接收到的数据放到packet"""
        self.writebytes(data)


def test_byte_array():
    """
        输出: [48 02 00 52 4E 41 4A A5 A5]
    """
    packet = ByteArray([0x48, 0x02])
    packet[2] = 0x00
    packet.writebytes([0x52, 0x4E])
    packet.write2byte(0x414A)
    packet.writebytes([0xa5, 0xa5])
    print(packet)


if __name__ == "__main__":
    test_byte_array()


