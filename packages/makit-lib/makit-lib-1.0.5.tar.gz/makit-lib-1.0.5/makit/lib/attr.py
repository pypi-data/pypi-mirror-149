#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: LiangChao
@email：liangchao@noboauto.com
@desc: 
"""
import re

from makit.lib import validate, fn
from makit.lib.validate import ValidateError


def rebuild_owner(owner):
    if hasattr(owner, '__described__'):
        return
    old_del = getattr(owner, '__del__', None)

    def __del__(self):
        for name in dir(owner):
            attr = getattr(owner, name)
            if isinstance(attr, Attr):
                attr.values.pop(id(self), None)
        if old_del:
            old_del(self)

    owner.__del__ = __del__
    owner.__described__ = True


class NULL:
    pass


class Attr:
    """
    描述器基类
    """

    def __init__(self, default=NULL, on_change=None, converter=None, validators=None, nullable=True,
                 readonly=False):
        self.name = None
        self._default = default
        self.values = {}
        self.__on_change = on_change
        self.converter = converter  # 值转换器
        self.validators = validators or []
        self.nullable = nullable
        self.readonly = readonly

    def __get__(self, instance, owner):
        rebuild_owner(owner)
        if instance is None:
            return self
        return self.get_value(instance)

    def __set__(self, instance, value):
        if self.readonly:
            raise Exception('attribute readonly!')
        old = self.get_value(instance)
        changed = old == value
        if self.converter:
            value = fn.run(self.converter, instance=instance, value=value)
        self.validate(instance, value)
        self.values[id(instance)] = value
        if changed:
            self.on_changed(instance, old, value)
        rebuild_owner(instance.__class__)

    def get_value(self, instance):
        return self.values.get(id(instance))

    def on_changed(self, instance, old, new):
        if self.__on_change:
            self.__on_change(instance, old, new)

    def validate(self, instance, value):
        raise_error = not hasattr(instance, 'errors')  # 如果实例没有errors，则校验抛异常
        if self.nullable and value is None:
            return True
        if not self.nullable and value is None:
            if self.name:
                message = f'"{self.name}" should not be None!'
            else:
                message = 'Invalid value: None'
            if raise_error:
                raise Exception(message)
            else:
                instance.errors.append(message)
        for v in self.validators:
            if hasattr(v, 'validate'):
                v = v.validate
            if callable(v):
                try:
                    fn.run(v, value, instance=instance)
                except Exception as e:
                    if raise_error:
                        raise
                    else:
                        instance.errors.append(f'"{self.name}" {e}' if self.name else str(e))
        return len(instance.errors) == 0


class StringAttr(Attr):
    def __init__(self, prefix=None, suffix=None, pattern=None, **kwargs):
        super().__init__(**kwargs)
        self.prefix = prefix
        self.suffix = suffix
        self.pattern = pattern

    def validate(self, instance, value):
        if self.prefix:
            self.validators.append(lambda v: should_startswith(v, self.prefix))
        if self.suffix:
            self.validators.append(lambda v: should_endswith(v, self.suffix))
        if self.pattern:
            self.validators.append(lambda v: should_match(v, self.pattern))
        super().validate(instance, value)


String = StringAttr


class IntAttr(Attr):
    def __init__(self, default=0, none=False, validators=None,
                 converter=None,
                 min=None, max=None):
        validators = (validators or []).append(lambda v: validate.check_int(v, min=min, max=max, raise_error=True))
        super().__init__(default=default, none=none, validators=validators, converter=converter)

    def validate(self, value):
        if not isinstance(value, int):
            raise ValidateError(f'{value} is not int!')
        super().validate(value)


Int = IntAttr


class FloatAttr(Attr):
    def __init__(self, default=0.0, none=False, validators=None, converter=None):
        super().__init__(
            default=default,
            none=none,
            validators=validators,
            converter=converter
        )

    def __set__(self, instance, value):
        Attr.__set__(self, instance, value)

    def validate(self, value):
        if not isinstance(value, float):
            raise ValidateError(f'{value} is not float!')
        super().validate(value)


Float = FloatAttr


class NumberAttr(Attr):
    def __init__(self, default=None, none=True, validators=None, converter=None):
        validators = (validators or []).append()
        super().__init__(
            default=default,
            none=none,
            validators=validators,
            converter=converter
        )


Number = NumberAttr


class BooleanAttr(Attr):
    def __init__(self, none=False, validator=None, **kwargs):
        validator = (validator or []).append(lambda v: none is True or isinstance(v, bool))
        super().__init__(none=none, validator=validator, **kwargs)


Boolean = BooleanAttr


class Type(Attr):
    def __init__(self, value_type, **kwargs):
        super().__init__(**kwargs)


# region validators

class Validator:
    def validate(self, value, attr):
        raise NotImplementedError


def should_startswith(value: str, prefixes):
    if not value.startswith(prefixes):
        raise Exception(f'should startswith: {prefixes}')


def should_endswith(value: str, suffix):
    if not value.endswith(suffix):
        raise Exception(f'should endswith: {suffix}')


def should_match(value: str, pattern):
    if re.match(pattern, value) is None:
        raise Exception(f'should match: {pattern}')


def not_none(value, attr):
    return value is not None


# endregion

class InvalidValidatorError(Exception):
    def __init__(self, model, attr, validator):
        self.model = model
        self.attr = attr
        self.validator = validator
