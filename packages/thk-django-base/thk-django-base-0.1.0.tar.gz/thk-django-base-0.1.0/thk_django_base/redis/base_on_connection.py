# -*- coding: utf-8 -*-
from abc import ABC

import redis


class BaseOnConnection(ABC):
    rdb: redis.Redis = None

    def __init__(self, rdb: redis.Redis = None):
        self.rdb = rdb or self.rdb
