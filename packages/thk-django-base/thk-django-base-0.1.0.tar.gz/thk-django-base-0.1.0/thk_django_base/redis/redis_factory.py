# -*- coding: utf-8 -*-
from typing import Dict, Optional
from django.conf import settings
from redis import Redis, ConnectionPool, Sentinel, RedisError


def _is_valid_redis_client(redis: Redis) -> bool:
    try:
        redis.ping()
        return True
    except RedisError:
        return False


class RedisFactory(object):
    _name2redis: Dict[str, Redis] = dict()
    _name2sentinel: Dict[str, Sentinel] = dict()
    _name2master_redis: Dict[str, Redis] = dict()
    _name2slave_redis: Dict[str, Redis] = dict()

    @classmethod
    def get_rdb(cls, name: str = 'default', readonly: bool = False) -> Redis:
        config = settings.REDIS[name]

        if config['type'] == 'standalone':
            redis: Optional[Redis] = cls._name2redis.get(name)
            if redis is None:
                connection_pool = ConnectionPool(**config['init'])
                redis = Redis(connection_pool=connection_pool)
                cls._name2redis[name] = redis
            return redis

        elif config['type'] == 'sentinel':
            # find cache
            if readonly:
                cache_redis = cls._name2slave_redis.get(name)
            else:
                cache_redis = cls._name2master_redis.get(name)
            # check
            if cache_redis is not None and _is_valid_redis_client(cache_redis):
                return cache_redis

            # new
            sentinel: Optional[Sentinel] = cls._name2sentinel.get(name)
            if sentinel is None:
                sentinel = Sentinel(**config['init'])
                cls._name2sentinel[name] = sentinel

            if readonly:
                slave_redis = sentinel.slave_for(**config['node'])
                cls._name2slave_redis[name] = slave_redis
                return slave_redis
            else:
                master_redis = sentinel.master_for(**config['node'])
                cls._name2master_redis[name] = master_redis
                return master_redis

        else:
            raise AssertionError(f"Invalid type {config['type']} in REDIS['{name}']")
