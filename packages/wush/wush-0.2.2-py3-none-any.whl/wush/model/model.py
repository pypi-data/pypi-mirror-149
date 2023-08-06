#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
基础模块
"""
import json

from wpy.base import BaseObject
from wush.model.datatype import DataType
from wush.model.datatype import Object

__FILTER_SET_FIELDS__ = set(('AUTO_FORMAT', 'DEFAULT_DATATYPE',
    '__is_format__',  '__datatype_dict__'))

class Model(BaseObject):

    AUTO_FORMAT = False     # 是否自动 format
    # 字段默认的 datatype
    DEFAULT_DATATYPE = None

    # 装载 Model 的 datatype 类型字段
    __datatype_dict__ = dict()
    # 对象是否已经进行过 format 操作
    __is_format__ = False


    def __init__(self, **kwargs):
        # 初始化 __datatype_dict__
        self.__datatype_dict__ = {}
        self.__add_datatype_dict__(**self.get_cls_datatype_dict())
        super().__init__(**kwargs)

        # 将未赋值的字段设置为 None
        for key in self.__datatype_dict__.keys():
            if key not in kwargs:
            #  if hasattr(self, key) and isinstance(getattr(self, key), DataType):
                self.__dict__[key] = None

        # 判断自动 format
        if self.AUTO_FORMAT:
            self.format()

    def __setattr__(self, key, value):
        #  """重载设置值的方法"""
        # 如果字段的默认模型存在，则设置值之前先添加 datatype
        if self.DEFAULT_DATATYPE:
            default_datatype = self.__build_default_datatype()
            self.__add_datatype_dict__(**{key: default_datatype})

        self.__dict__[key] = value

    def get_cls_datatype_dict(self):
        item = {}
        for key, value in self.__class__.__dict__.items():
            if not isinstance(value, DataType):
                continue
            item[key] = value
        return item

    def __add_datatype_dict__(self, **kwargs):
        for k, v in kwargs.items():
            if k in __FILTER_SET_FIELDS__:
                continue
            if not isinstance(v, DataType):
                continue
            self.__datatype_dict__[k] = v

    def __build_default_datatype(self):
        """构建默认的 datatype"""
        return self.DEFAULT_DATATYPE

    def format(self):
        """将 datatype 字段进行格式化处理"""
        self._format(self)

    def _format(self, model):
        """嵌套 format"""
        # 判断是否有默认字段
        # 并对对象中存在的赋值添加到 __datatype_fields__ 中

        for k in model.__datatype_dict__.keys():
            # 格式化单个字段
            self._format_field(model, k)

        model.__dict__['__is_format__'] = True

    def _format_field(self, model, field):
        """格式化 field"""
        # 如果 field 不是 datatype 类型，直接返回
        #  datatype_fields = model.__get_datatype_fields()
        datatype_fields = model.__datatype_dict__
        dt_ins = datatype_fields.get(field)
        if not dt_ins:
            return

        try:
            value = model.__dict__.get(field)
            dt_ins.set_value(value)
        except:
            pass
        # 校验
        dt_ins.valid()
        set_val = dt_ins.value()
        # 清空数据
        dt_ins.clear()
        model.__dict__[field] = set_val
        # 嵌套 format
        if isinstance(set_val, Model):
            #  self._format(set_val)
            set_val.format()

    def dict(self):
        return self.to_dict()

    def to_dict(self):
        """
        将实例转为 dict 数据
        执行前需要保证实例已经执行过 format 方法或设置成员变量 AUTO_FORMAT=True
        """
        return self._to_dict(self)

    @classmethod
    def _to_dict(cls, model):
        """对 Model 进行循环 to_dict 操作"""
        data = {}
        #  for key in model.__get_datatype_fields().keys():
        for key in model.__datatype_dict__.keys():
            if not hasattr(model, key):
                continue
            origin_value = getattr(model, key)
            if isinstance(origin_value, Model):
                data[key] = origin_value.to_dict()
            else:
                data[key] = origin_value
        return data

    def to_json(self):
        return json.dumps(self, default=lambda o: o.to_dict(), sort_keys=True)

    def json(self):
        return self.to_json()

from wush.model import datatype
class Person(Model):
    AUTO_FORMAT = True
    id = datatype.Int(default=10)

class Book(Model):
    name = datatype.Str(default='book')

class User(Model):
    AUTO_FORMAT = True
    DEFAULT_DATATYPE = Object(model = Book)
    name = datatype.Str(default='wxnacy')

class Field(Model):
    doc = datatype.Str()
    _type = datatype.Object()
    value = datatype.Object()

class Json(Model):
    DEFAULT_DATATYPE = datatype.Object(model = Field)

    cust_field = datatype.Str(default='cust')

class Request(Model):
    json = datatype.Object(model=Json)

if __name__ == "__main__":
    #  p = Person()
    #  print(p.__datatype_dict__)
    #  print(p.id)
    #  assert p.id == 10

    #  b = Book()
    #  b.format()
    #  print(b.__datatype_dict__)
    #  print(b.name)
    #  assert b.name == 'book'

    u = User()
    assert u.name == 'wxnacy'
    u.book = { "name": "b1" }
    u.format()
    print(u.to_dict())
    #  assert u.book.name == 'b1'

    u1 = User()
    u1.book1 = { "name": "b2" }
    print(u1.to_dict())
