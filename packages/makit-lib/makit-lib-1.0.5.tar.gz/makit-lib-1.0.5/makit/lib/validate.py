#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: LiangChao
@email：liangchao@noboauto.com
@desc: 
"""


def not_none(value, raise_error=False):
    if value is None:
        if raise_error:
            raise ValidateError(f'{value} should not be None!')
        return False
    return True


def check_int(value, min=None, max=None, raise_error=False):
    if not isinstance(value, int):
        if raise_error:
            raise ValidateError(f'{value} is not int!')
        return False
    if min and value < min:
        if raise_error:
            raise ValidateError(f'{value} should be greater than {min}')
        return False
    if max and value > max:
        if raise_error:
            raise ValidateError(f'{value} should be less than {max}')
        return False
    return True


class ValidateError(Exception):
    """"""
