# -*- coding: utf-8 -*-
from typing import Union
from .base_structure import BaseStructure


class Hash(BaseStructure):

    def __setitem__(self, key: str, value: str):
        self.set_member(key, value)

    def __getitem__(self, key: str) -> str:
        return self.get_member_by_key(key)

    def __delitem__(self, key: str):
        self.delete_by_key(key)

    def get_length(self) -> int:
        return self.rdb.hlen(self.main_key)

    def get_all_members(self) -> dict:
        return self.rdb.hgetall(self.main_key)

    def get_all_keys(self) -> list:
        return self.rdb.hkeys(self.main_key)

    def get_member_by_key(self, key: str) -> str:
        return self.rdb.hget(self.main_key, key)

    def set_member(self, key: str, value: str) -> int:
        # 返回是否是新增
        return self.rdb.hset(self.main_key, key, value)

    def set_member_must_new(self, key: str, value: str) -> bool:
        return self.rdb.hsetnx(self.main_key, key, value)

    def set_multi_members(self, mapping: dict) -> int:
        return self.rdb.hset(self.main_key, mapping=mapping)

    def exists_member(self, key: str) -> bool:
        return self.rdb.hexists(self.main_key, key)

    def delete_by_key(self, key: Union[str, list]) -> int:
        if isinstance(key, list):
            return self.rdb.hdel(self.main_key, *key)
        else:
            return self.rdb.hdel(self.main_key, key)

    def increase_member(self, key: str, amount: int = 1) -> int:
        return self.rdb.hincrby(self.main_key, key, amount)
