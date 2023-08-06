# -*- coding: utf-8 -*-

ALL_METHOD = {'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'}
DETAIL_METHOD_GROUP = {
    'dynamic_method': ['GET', 'PUT', 'DELETE', 'PATCH'],
    'static_method': ['POST', 'OPTION']
}
LIST_METHOD_GROUP = {
    'dynamic_method': ['PUT', 'DELETE', 'PATCH'],
    'static_method': ['GET', 'POST', 'OPTION']
}
DEFAULT_METHOD_MAP = {'get': 'get', 'post': 'post', 'put': 'put', 'patch': 'patch', 'delete': 'delete', 'head': 'head',
                      'options': 'options'}

LOOKUP_SEP = '__'

LIST_SERIALIZER_KWARGS = (
    'read_only',
    'write_only',
    'required',
    'allow_null',
    'default',
    'source',
    'validators',
    'error_messages',
    'label',
    'description',
    'instance',
    'data',
    'partial'
)
ALL_FIELDS = '__all__'
