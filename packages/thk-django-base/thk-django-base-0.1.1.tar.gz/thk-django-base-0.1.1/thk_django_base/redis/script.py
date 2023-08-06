# -*- coding: utf-8 -*-
from typing import Union
import redis

from .base_on_connection import BaseOnConnection


class Script(BaseOnConnection):

    def __init__(self, lua_content: str, rdb: redis.Redis = None):
        super().__init__(rdb=rdb)

        self._lua_content = lua_content
        self._script = self.rdb.register_script(self._lua_content)

    def execute(self, key_list: list, value_list: list) -> Union[str, int, list]:
        return self._script(key_list, value_list)
