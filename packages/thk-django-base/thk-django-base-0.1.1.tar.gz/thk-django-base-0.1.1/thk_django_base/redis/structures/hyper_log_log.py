# -*- coding: utf-8 -*-
from typing import Union
from .base_structure import BaseStructure


class HyperLogLog(BaseStructure):

    def add(self, member: Union[str, list]) -> int:
        # 如果至少有1个元素被添加返回1， 否则返回0
        if isinstance(member, list):
            return self.rdb.pfadd(self.main_key, *member)
        else:
            return self.rdb.pfadd(self.main_key, member)

    def get_length(self) -> int:
        return self.rdb.pfcount(self.main_key)
