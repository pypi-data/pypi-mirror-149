#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: LiangChao
@email：liangchao@noboauto.com
@desc: 
"""
from contextlib import contextmanager


class ContextZip:
    """
    用于合并两个contextmanager装饰的方法，需要注意被合并的上下文方法必须参数一致

    用法：
        ctx = ContextZip()

        @ctx.contextmanager
        def f1():
            pass

        @ctx.contextmanager
        def f1():
            pass

        with ctx():
            ...
    """
    def __init__(self, error_callback=None):
        self.ctx_funcs = []
        self.error_callback = error_callback

    @contextmanager
    def __call__(self, *args, **kwargs):
        gens = []
        for f in self.ctx_funcs:
            gens.append(f(*args, **kwargs))

        outputs = []
        for g in gens:
            output = g.__enter__()
            outputs.append(output)

        yield tuple(outputs)

        for g in reversed(gens):
            g.__exit__(None, None, None)

    def contextmanager(self, func):
        cm = contextmanager(func)
        self.ctx_funcs.append(cm)
        return cm

    def zip(self, *funcs):
        self.ctx_funcs.extend(funcs)
        return self


def zip_context(*contexts):
    ctx_zip = ContextZip()
    ctx_zip.ctx_funcs.extend(contexts)
    return ctx_zip
