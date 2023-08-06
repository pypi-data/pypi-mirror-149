# -*- coding: utf-8 -*-
import time
import logging
import asyncio
from threading import Lock
from typing import Union, Any, Dict
from aredis import StrictRedis, StrictRedisCluster


class SingletonMeta(type):
    """元类——有限的单例模式
    当初始化参数包含new=True时，将构造一个新的对象
    """
    __instance = None
    __lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            new = kwargs.pop('new', None)
            if new is True:
                return super().__call__(*args, **kwargs)
            if not cls.__instance:
                cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class MemoryEngine:
    """本地内存作为后端缓存引擎，不支持分布式
    只支持get、set方法
    """

    def __init__(self):
        self.namespace = {}
        self._check_time = 0
        self._check_interval = 60

    def delete(self, key: str) -> None:
        """删除指定缓存"""
        if key in self.namespace:
            del self.namespace[key]

    def et_clear(self) -> None:
        """清理超时缓存"""
        clear_names = []
        if time.time() > self._check_time + self._check_interval:
            self._check_time = time.time()
            for name, block in self.namespace.items():
                if block.ttl < -1:
                    clear_names.append(name)
        for name in clear_names:
            del self.namespace[name]

    async def ttl(self, name) -> int:
        self.et_clear()
        if name not in self.namespace:
            return -1
        return int(self.namespace[name].ttl)

    async def get(self, name):
        self.et_clear()
        if name not in self.namespace:
            return None
        return self.namespace[name].val

    async def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        if nx and name in self.namespace:
            return
        if xx and name not in self.namespace:
            return
        self.namespace[name] = DataBlock(name, value, ex, px)
        if len(value) > 16384 and (ex or px):
            # 实验性功能 大容量缓存清理机制 避免长时间不使用缓存下占用内存
            life = ex if ex else px // 1000
            loop = asyncio.get_event_loop()
            loop.call_later(life * 2, self.delete, name)


class DataBlock:
    """内存数据块 封装了有效期"""

    def __init__(self, name: str, value: Any, ex: float = None,
                 px: float = None):
        """
        :param name: key名
        :param value: 存储value
        :param ex: 生命周期，单位秒
        :param px: 生命周期，单位毫秒
        """
        self._name = name
        self._value = value
        self.et = time.time() - 1
        if ex:
            self.et += ex
        if px:
            self.et += (px / 1000)
        if not ex and not px:
            self._ttl = -1

    @property
    def val(self):
        return self._value if self.ttl >= -1 else None

    @property
    def ttl(self):
        if hasattr(self, '_ttl'):
            return self._ttl
        return self.et - time.time()

    def __repr__(self):
        return f'<name={self._name}>'


class Cache(metaclass=SingletonMeta):
    """一个基于redis封装的异步缓存类，它可以快速方便切换多个缓存库
    Cache类默认使用default缓存库，你可以使用select(db_name)切换其他库，并且select支持
    链式调用，但select方法并不会改变原对象指向的default缓存库
    Cache对象通过反射拥有了StrictRedis和StrictRedisCluster类下的所有方法，你可以直接对
    对象执行redis命令，此外Cache还封装了一个方法execute(command, *args, **kwargs)
    相比于反射方法，使用execute方法会自动对返回数据解码
    针对字符串类型，Cache对get和set方法作了优化，当使用get和set方法时，可以同时传递一个序列化器，
    它会查询和存储时自动使用序列化器，也就是说你可以使用set方法存储任意序列化器支持的对象
    """
    logger = logging.getLogger(__name__)

    def __init__(self, config: dict):
        """
        :param config: 缓存数据库字典
        :return: Cache对象
        """
        self._default = 'default'
        self._caches = {}
        serializer = config.pop('serializer', 'ujson')
        try:
            self.serializer = __import__(serializer)
        except:
            self.serializer = __import__('json')
        for key, value in config.items():
            try:
                if value.get('engine') == 'memory':
                    self._caches[key] = MemoryEngine()
                elif 'startup_nodes' in value:
                    self._caches[key] = StrictRedisCluster(**value)
                else:
                    self._caches[key] = StrictRedis(**value)
            except Exception as e:
                self.logger.error(e)

    @property
    def all(self) -> Dict[str, Union[StrictRedis, StrictRedisCluster]]:
        """返回全部缓存数据库"""
        return self._caches

    @property
    def current_db(self) -> Union[StrictRedis, StrictRedisCluster]:
        """返回缓存对象指向的缓存数据库"""
        return self._caches[self._default]

    def select(self, name: str = 'default') -> 'Cache':
        """获取指定缓存数据库
        支持多次链式调用select方法
        永远不会改变app所绑定的默认缓存数据库
        :param name: 定义的数据库名，默认值为"default"
        :return: Cache对象
        """
        if name not in self._caches:
            raise AttributeError(f'Cache database "{name}" not found. '
                                 f'Please check CACHES config in settings')
        obj = Cache(config={}, new=True)
        obj._caches = self._caches
        obj._default = name
        return obj

    async def execute(self, command: str, *args, **kwargs) -> Any:
        """实现结果自解码
        :param command: 执行的redis原生命令
        :return: 返回redis结果的utf8解码
        """
        if hasattr(StrictRedis, command):
            result = await getattr(self, command)(*args, **kwargs)
            if result:
                result = result.decode('utf8')
            return result
        else:
            raise getattr(self, command)

    async def get(self, name, serializer=None, **kwargs) -> Any:
        """覆盖redis的字符串get方法，提供序列化能力
        :param name: key
        :param serializer: 使用指定的序列化模块
        :param kwargs: 传递给序列化方法
        :return: 返回redis结果的反序列化对象
        """
        if not serializer:
            serializer = self.serializer
        value = await self.current_db.get(name)
        if not value:
            return None
        else:
            if isinstance(value, bytes):
                value = value.decode('utf8')
        try:
            return serializer.loads(value, **kwargs)
        except ValueError:
            return value

    async def set(self, name: str, value: Any, serializer=None,
                  ex=None, px=None, nx=False, xx=False, **kwargs) -> bool:
        """永远在redis层以string格式存储，提供反序列化能力
        :param name:
        :param value:
        :param serializer: 使用指定的序列化模块
        :param ex: 设置键key的过期时间，单位为秒
        :param px: 设置键key的过期时间，单位为毫秒
        :param nx: 只有键key不存在的时候才会设置key的值
        :param xx: 只有键key存在的时候才会设置key的值
        :param kwargs: 传递给反序列化方法
        :return: 执行结果
        """
        if not serializer:
            serializer = self.serializer
        _kwargs = {'ensure_ascii': True}
        _kwargs.update(kwargs)
        if not isinstance(value, str):
            value = serializer.dumps(value, **_kwargs)
        return await self.current_db.set(name, value, ex, px, nx, xx)

    def handle(self, backed: str):
        # TODO 查询缓存库

        # TODO 执行handler获取结果

        # TODO 返回结果并存储至缓存
        """提供给视图方法的装饰器 它缓存视图方法返回的结果"""

    def __getitem__(self, item) -> 'Cache':
        return self.select(item)

    def __getattr__(self, attr) -> Any:
        return getattr(self.current_db, attr)
