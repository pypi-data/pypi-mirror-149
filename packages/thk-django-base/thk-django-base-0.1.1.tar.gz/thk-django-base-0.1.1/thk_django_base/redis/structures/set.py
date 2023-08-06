# -*- coding: utf-8 -*-
from typing import Union

from .base_structure import BaseStructure


class Set(BaseStructure):

    def add_member(self, member: Union[str, list]) -> int:
        # 返回成功add的个数
        if isinstance(member, list):
            return self.rdb.sadd(self.main_key, *member)
        else:
            return self.rdb.sadd(self.main_key, member)

    def pop(self) -> str:
        return self.rdb.spop(self.main_key)

    def remove_member(self, member: Union[str, list]) -> int:
        # 返回删除的个数
        if isinstance(member, list):
            return self.rdb.srem(self.main_key, *member)
        else:
            return self.rdb.srem(self.main_key, member)

    def get_length(self) -> int:
        return self.rdb.scard(self.main_key)

    def get_all_members(self) -> set:
        return self.rdb.smembers(self.main_key)

    def is_member(self, member: str) -> bool:
        return self.rdb.sismember(self.main_key, member)

    def move_to(self, another_set_main_key: str, member: str) -> bool:
        return self.rdb.smove(self.main_key, another_set_main_key, member)
