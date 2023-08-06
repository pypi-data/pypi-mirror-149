# -*- coding: utf-8 -*-
from typing import Union
from .base_structure import BaseStructure


class String(BaseStructure):

    def get(self) -> str:
        return self.rdb.get(self.main_key)

    def set(self, value: Union[str, int]) -> bool:
        return self.rdb.set(self.main_key, value)

    def set_if_not_exists(self, value: Union[str, int]) -> bool:
        return self.rdb.setnx(self.main_key, value)

    def increase(self, amount: int = 1) -> int:
        return self.rdb.incr(self.main_key, amount)
