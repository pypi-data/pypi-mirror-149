#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: LiangChao
@email：liangchao@noboauto.com
@desc: 用于配置管理，支持继承，也可以将不同框架的配置集成在一起使用
"""
import inspect


class _NotExists:
    """"""


class Settings:
    """
    配置
    """
    def __init__(self, user_settings=None, defaults=None, bases=None):
        self.bases = bases or []
        self._user_settings = user_settings
        self._defaults = defaults

    def __getattr__(self, item):
        value = _NotExists
        if self._user_settings:
            value = self.__get_value(self._user_settings, item)
        if value is _NotExists and self._defaults:
            value = self.__get_value(self._defaults, item)
        if value is _NotExists and self.bases:
            for base in self.bases:
                value = self.__get_value(base, item)
                if value is not _NotExists:
                    break
        if value is _NotExists:
            raise SettingsNotFoundError(item)
        return value

    def __get_value(self, obj, name):
        if inspect.ismodule(obj):
            value = getattr(obj, name, _NotExists)
        elif isinstance(obj, dict) and name in obj:
            value = obj.get(name, _NotExists)
        else:
            value = getattr(obj, name, _NotExists)
        return value

    def __call__(self, user_settings=None, defaults=None, bases=None):
        if not bases:
            bases = [self]
        return Settings(user_settings, defaults, bases)


settings = Settings()


class SettingsNotFoundError(Exception):
    """"""
