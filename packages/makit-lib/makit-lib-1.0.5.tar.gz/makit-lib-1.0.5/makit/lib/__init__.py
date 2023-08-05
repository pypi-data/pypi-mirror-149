# coding=utf-8

"""
@Author: LiangChao
@Email: kevinleong1011@hotmail.com
@Created: 2022/1/25
@Desc: 
"""
import threading
from typing import Iterable

from ._data import Data
from ._dict import *
from ._input import *
from ._json import *
from ._serialize import serialize
from ._settings import settings as build_settings
from ._time import Timeout
from . import _doc as pydoc


class Str(str):
    def __new__(cls, o, *args, **kwargs):  # 重写 __new__ 否则无法正常重写 __init__
        return super().__new__(cls, o)


def singleton(o):
    """
    对类添加单例装饰，不需要专门写__new__实现，也不影响自己的__new__
    """
    o._instance = None
    o._lock = threading.Lock()

    origin_new = getattr(o, '__new__', None)
    origin_init = getattr(o, '__init__', None)

    def class_new(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = object.__new__(cls)
                cls._instance._initialized = False

            if origin_new:
                origin_new(cls, *args, **kwargs)
            return cls._instance

    o.__new__ = class_new

    # 这里保证实例初始化只会执行一次，否则即使保证了实例也无法保证实例内部数据
    def init(self, *args, **kwargs):
        if not self._initialized:
            origin_init(self, *args, **kwargs)
            self._initialized = True

    o.__init__ = init

    return o


def iterate(iterable, convert=None, stop=None, skip=None):
    """
    迭代器
    :param iterable: 可迭代对象
    :param convert: 迭代时的转换器，必须是 callable 对象或者实现 convert 函数
    :param stop: 用于终止迭代，支持callable和iterable
    :param skip: 用于迭代时跳过，支持callable和iterable
    :return:
    """

    def check(f):
        if callable(f) and f(item):
            return True
        elif isinstance(f, Iterable) and item in f:
            return True
        elif item == f:
            return True

    for item in iterable:
        if callable(convert):
            item = convert(item)
        elif hasattr(convert, 'convert'):
            item = convert.convert(item)
        else:
            raise RuntimeError('convert must be callable or has implement method: convert.')
        if stop:
            if check(stop):
                return
        if skip:
            if check(skip):
                continue
        yield item
