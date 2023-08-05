#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: LiangChao
@email：liangchao@noboauto.com
@desc: 对platform进行扩展，同时可以直接调用原有方法
"""
import platform


def format(fmt: str):
    """
    格式化输出平台信息\n

    - %s  - 系统，System name
    - %m  - 处理器, platform machine name
    - %r  - 系统release版本， System release version
    - %v  - 系统版本号, System version
    - %n  - 局域网节点名称， node in local network
    - %pv - Python版本, Python version
    - %b  - 系统位数，System bits

    :param fmt:
    :return:
    """
    if '%s' in fmt:
        fmt = fmt.replace('%s', platform.system())
    if '%m' in fmt:
        fmt = fmt.replace('%m', platform.machine())
    if '%v' in fmt:
        fmt = fmt.replace('%v', platform.version())
    if '%n' in fmt:
        fmt = fmt.replace('%n', platform.node())
    if '%r' in fmt:
        fmt = fmt.replace('%r', platform.release())
    if '%pv' in fmt:
        fmt = fmt.replace('%pv', platform.python_version())
    if '%b' in fmt:
        fmt = fmt.replace('%b', platform.architecture()[0])
    return fmt


def __getattr__(name):
    return getattr(platform, name)
