# -*- coding: utf-8 -*-
import collections
from collections.abc import MutableMapping


class BindingDict(MutableMapping):
    """
    这个类似于dict的对象用于在序列化器中存储字段。
    这确保了无论何时将字段添加到我们调用的序列化器中
    field.bind() 使 field_name 和 parent 属性可以正确设置。
    """

    def __init__(self, serializer):
        self.serializer = serializer
        self.fields = collections.OrderedDict()

    def __setitem__(self, key, field):
        self.fields[key] = field
        field.bind(field_name=key, parent=self.serializer)

    def __getitem__(self, key):
        return self.fields[key]

    def __delitem__(self, key):
        del self.fields[key]

    def __iter__(self):
        return iter(self.fields)

    def __len__(self):
        return len(self.fields)

    def __repr__(self):
        return dict.__repr__(self.fields)

# def set_value(instance, key, value):
#     if isinstance(value, Mapping):
#         for k, v in value.items():
#             set_value(instance, k, v)
#     setattr(instance, key, value)
