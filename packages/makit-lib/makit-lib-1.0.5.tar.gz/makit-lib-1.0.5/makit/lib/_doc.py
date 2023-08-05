#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: LiangChao
@email：liangchao@noboauto.com
@desc: 
"""
import re
from collections import namedtuple

FuncDoc = namedtuple('FuncDoc', ('name', 'description', 'args'))


def parse_func(func):
    args = {}
    doc = func.__doc__
    temp = []
    for line in doc.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(':param '):
            p = re.compile(r':param ([a-zA-Z_0-9]+):\s*(.*)\s*')
            matches = p.findall(line)
            for match in matches:
                if len(match) > 1:
                    args[match[0]] = match[1]
                else:
                    args[match[0]] = None
        elif line.startswith(':return:'):
            pass
        else:
            temp.append(line)
    return FuncDoc(name=func.__name__, description='\n'.join(temp), args=args)
