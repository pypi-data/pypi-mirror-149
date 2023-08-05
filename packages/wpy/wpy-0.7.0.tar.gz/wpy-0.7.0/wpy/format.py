#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:


__all__ = [
    'format_float',
    'format_seconds',
    'format_size',
]

class Format(object):

    @classmethod
    def format_seconds(cls, seconds: int):
        """秒数"""
        #  suffixs = ('B', 'K', 'M', 'G', 'T')
        #  for i in range(5):
            #  if size < 1024 ** ( i + 1 ):
                #  bei_chu = 1024 ** i or 1
                #  res_num = size / bei_chu
                #  if cls._is_int(res_num):
                    #  return '{}{}'.format(int(res_num), suffixs[i])
                #  else:
                    #  return '{:0.2f}{}'.format(res_num, suffixs[i] )
        #  return '{}B'.format(size)

    @classmethod
    def format_size(cls, size: int):
        """格式化文件大小"""
        suffixs = ('B', 'K', 'M', 'G', 'T')
        for i in range(5):
            if size < 1024 ** ( i + 1 ):
                bei_chu = 1024 ** i or 1
                res_num = size / bei_chu
                if cls._is_int(res_num):
                    return '{}{}'.format(int(res_num), suffixs[i])
                else:
                    return '{:0.2f}{}'.format(res_num, suffixs[i] )
        return '{}B'.format(size)

    @classmethod
    def format_float(cls, float_val, decimal_digits=2):
        """格式化 float 数据"""
        if not float_val:
            return float_val
        fmt = '{{:0.{}f}}'.format(decimal_digits)
        return float('{:0.2f}'.format(float_val))

    @classmethod
    def _is_int(cls, num):
        if isinstance(num, int):
            return True
        if isinstance(num, float):
            suffix = str(num).split('.')[-1]
            if len(suffix) > 1:
                return False
            if suffix == '0':
                return True
        return False


format_seconds = Format.format_seconds
format_size = Format.format_size
format_float = Format.format_float


