# -*- coding: utf-8 -*-
from typing import Union

from .base_structure import BaseStructure


class List(BaseStructure):

    def get_length(self) -> int:
        return self.rdb.llen(self.main_key)

    def get_all_members(self) -> list:
        return self.rdb.lrange(self.main_key, 0, -1)

    def get_member_by_index(self, index: int) -> str:
        return self.rdb.lindex(self.main_key, index)

    def right_push(self, data: Union[str, list], need_exists: bool = False) -> int:
        if need_exists:
            func = self.rdb.rpushx
        else:
            func = self.rdb.rpush

        if isinstance(data, list):
            return func(self.main_key, *data)
        else:
            return func(self.main_key, data)

    def left_push(self, data: Union[str, list], need_exists: bool = False) -> int:
        if need_exists:
            func = self.rdb.lpushx
        else:
            func = self.rdb.lpush

        if isinstance(data, list):
            return func(self.main_key, *data)
        else:
            return func(self.main_key, data)

    def right_pop(self) -> str:
        return self.rdb.rpop(self.main_key)

    def left_pop(self) -> str:
        return self.rdb.lpop(self.main_key)

    def block_left_pop(self, timeout_seconds: int = 0) -> str:
        result = self.rdb.blpop(self.main_key, timeout_seconds)
        if isinstance(result, tuple) and len(result) == 2:
            return result[1]

    def block_right_pop(self, timeout_seconds: int = 0) -> str:
        result = self.rdb.brpop(self.main_key, timeout_seconds)
        if isinstance(result, tuple) and len(result) == 2:
            return result[1]

    def remove_member(self, member: str, count: int = 0) -> int:
        return self.rdb.lrem(self.main_key, count, member)

    def right_pop_left_push(self, another_list_main_key: str) -> str:
        return self.rdb.rpoplpush(self.main_key, another_list_main_key)

    def block_right_pop_left_push(self, another_list_main_key: str, timeout_seconds: int = 0) -> str:
        return self.rdb.brpoplpush(self.main_key, another_list_main_key, timeout_seconds)
