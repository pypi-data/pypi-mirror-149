# coding=utf-8

"""
@Author: LiangChao
@Email: kevinleong1011@hotmail.com
@Desc: 
"""
from enum import Enum

from deprecated.sphinx import deprecated


@deprecated(version='1.0.4', reason='请使用标准方式：Enum(value)')
def from_value(enum_type, value):
    """
    从枚举值获取枚举，一般用于反向转换
    :param enum_type:
    :param value:
    :return:
    """
    members = enum_type.__members__
    for k, v in members.items():
        if value == v.value:
            return v


@deprecated(version='1.0.4', reason='请使用标准方式：Enum.__members__["name"]')
def from_name(enum_type, name, return_default=False):
    """
    根据名称获取枚举对象，一般用于反向转换
    :param enum_type:
    :param name:
    :param return_default:
    :return:
    """
    members = enum_type.__members__
    first_member = None
    for k, v in members.items():
        if not first_member:
            first_member = v
        if k == name:
            return v
    if return_default:
        return first_member


class EnumMixin:

    @classmethod
    def items(cls: Enum):
        return cls.__members__.items()

    @classmethod
    def from_name(cls: Enum, name, default=None, ign_case=False):
        """

        :param name:
        :param default:
        :param ign_case:
        :return:
        """
        members = cls.__members__
        for k, v in members.items():
            if k == name:
                return v
            elif ign_case and k.lower() == name.lower():
                return v
        if default is not None:
            return default
        else:
            raise Exception(f'"{name}" is not defined by {cls.__name__}')
