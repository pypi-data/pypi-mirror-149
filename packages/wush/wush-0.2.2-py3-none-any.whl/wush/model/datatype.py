#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
基础模块
"""

from wpy.base import BaseObject
from wpy.base import BaseEnum

# TODO 改为抽象类
class DataType(BaseObject):
    _value = None       # 对象实例化或手动设置的值
    _type = object      # 字段赋值时应该给予的类型
    _default = None     # 当前类型的默认值
    _name = None        # 字段名称

    default = None      # 使用时赋值的默认数据
    convert = False     # 是否强制转换当前类型

    @property
    def name(self):
        return self._name

    def set_value(self, value):
        self._value = value
        # 强制转换类型
        if self.convert:
            self._value = self._type(self._value)

    def value(self):
        """获取数据"""
        val = str(self.default()) if callable(self.default) else self.default
        # 只有等 None 的时候才会返回默认值
        if self._value == None:
            return val or self._default
        return self._value # or val or self._default

    def clear(self):
        """清空数据"""
        self._value = None

    @property
    def _value_fmt(self):
        return f'{self.name}:{self._value}'

    def valid(self):
        """校验赋值"""
        if self._value != None and not isinstance(self._value, self._type):
            raise ValueError(f'{self._value_fmt} is not be {self._type}')

    @classmethod
    def get_base_datatype(cls, basetype):
        """获取基础类型类"""
        for clz in cls.__subclasses__():
            if clz._type == basetype:
                return clz
        raise ValueError(f'{basetype} is not basetype')


class Str(DataType):
    _type = str
    _default = str()

    enum = None
    upper = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.enum and not issubclass(self.enum, BaseEnum):
            raise ValueError('enum must be wpy.base.BaseEnum')

    def set_value(self, value):
        super().set_value(value)
        if self.upper and self._value:
            self._value = self._value.upper()

    def valid(self):
        super().valid()
        if self.enum and self._value != None and \
                self._value not in self.enum.values():
            raise ValueError(f'{self._value_fmt} is not {self.enum}')


class Int(DataType):
    _type = int
    _default = int()


class Float(DataType):
    _type = float
    _default = float()


class Dict(DataType):
    _type = dict
    _default = dict()


class List(DataType):
    _type = list
    _default = list()

    model = None

    def value(self):
        """获取数据"""
        if self.model and self._value:
            items = []
            for item in self._value:
                items.append(self.model(**item))
            return items

        return super().value()

class Object(DataType):
    _type = object

    model = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.model:
            self._default = self.model()

    def valid(self):
        """校验"""
        super().valid()
        if self._value != None and self.model:
            # 如果当前类型已经格式化，不在执行检查
            if isinstance(self._value, self.model):
                return
            if not isinstance(self._value, dict):
                raise ValueError(f'{self._value_fmt} can not to {self.model}')

    def value(self):
        """获取数据"""
        if self.model and self._value != None:
            # 对于已经格式化的数据不再重复执行
            if isinstance(self._value, self.model):
                return self._value
            return self.model(**self._value)

        return super().value()
