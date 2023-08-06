# -*- coding: utf-8 -*-
from typing import Callable, Union
from numbers import Number

from .base_structure import BaseStructure


class SortedSet(BaseStructure):

    # 没有set_member，add就能起到set的效果
    def add(
            self, key: str, score: Union[Number, str],
            only_add: bool = False, only_update: bool = False, change_return: bool = False
    ) -> int:
        return self.add_list({key: score}, only_add, only_update, change_return)

    def add_list(
            self, mapping: dict,
            only_add: bool = False, only_update: bool = False, change_return: bool = False
    ):
        """
        Args:
            mapping: key, store的列表
            only_add: 不会更新存在元素，只会增加新元素
            only_update: 只更新存在元素，不会增加新元素
            change_return: 原来返回值的意思是，新增的元素数; 使用这个参数后，返回值的意思是修改的元素数
        Returns:
            见 change_return

        """
        return self.rdb.zadd(self.main_key, mapping, nx=only_add, xx=only_update, ch=change_return)

    def get_length(self) -> int:
        return self.rdb.zcard(self.main_key)

    def pop_max(self, count: int = 1) -> list:
        return self.rdb.zpopmax(self.main_key, count)

    def pop_min(self, count: int = 1) -> list:
        return self.rdb.zpopmin(self.main_key, count)

    def block_pop_max(self, timeout: int = 0) -> list:
        # 0代表一直等，这个只能同时等一个
        values = self.rdb.bzpopmax(self.main_key, timeout)
        if values is not None:
            return [(values[1], values[2])]

    def block_pop_min(self, timeout: int = 0) -> list:
        values = self.rdb.bzpopmax(self.main_key, timeout)
        if values is not None:
            return [(values[1], values[2])]

    def get_count_between_scores(self, min_score, max_score) -> int:
        """
        可以像下面member一样，拼接[、(成字符串
        Args:
            min_score: 有个特殊值，-inf 代表最小值
            max_score: 有个特殊值, +inf 代表最大值

        Returns:

        """
        return self.rdb.zcount(self.main_key, min_score, max_score)

    def increase_member(self, key: str, amount: Number = 1) -> float:
        # 返回increase后的值
        return self.rdb.zincrby(self.main_key, amount, key)

    def get_count_between_members(self, min_member: str, max_member: str) -> int:
        """
        member名前需要加 [、(，与数学上的概念相同：包含、不包含当前值
        Args:
            min_member: 有个特殊值，- 代表最小值
            max_member: 有个特殊值, + 代表最大值

        Returns:

        """
        return self.rdb.zlexcount(self.main_key, min_member, max_member)

    def get_member_list(
            self, start_index: int, stop_index: int,
            with_scores: bool = False, score_cast_func: Callable = float,
            desc: bool = False
    ) -> list:
        return self.rdb.zrange(
            self.main_key, start_index, stop_index,
            desc=desc, withscores=with_scores, score_cast_func=score_cast_func
        )

    def get_member_list_between_members(
            self, min_member: str, max_member: str,
            offset: int = None, count: int = None,
            desc: bool = False
    ) -> list:
        if not desc:
            func = self.rdb.zrangebylex
        else:
            func = self.rdb.zrevrangebylex
            min_member, max_member = max_member, min_member
        return func(self.main_key, min_member, max_member, offset, count)

    def get_member_list_between_scores(
            self, min_score, max_score,
            offset: int = None, count: int = None,
            with_scores: bool = False, score_cast_func: Callable = float,
            desc: bool = False
    ) -> list:
        if not desc:
            func = self.rdb.zrangebyscore
        else:
            func = self.rdb.zrevrangebyscore
            min_score, max_score = max_score, min_score

        return func(self.main_key, min_score, max_score, offset, count, with_scores, score_cast_func)

    def get_rank(self, member: str, desc: bool = False) -> int:
        if not desc:
            func = self.rdb.zrank
        else:
            func = self.rdb.zrevrank

        return func(self.main_key, member)

    def remove_member(self, member: str) -> int:
        return self.rdb.zrem(self.main_key, member)

    def remove_member_list_between_members(self, min_member: str, max_member: str):
        return self.rdb.zremrangebylex(self.main_key, min_member, max_member)

    def remove_member_list_between_scores(self, min_score, max_score):
        return self.rdb.zremrangebyscore(self.main_key, min_score, max_score)

    def remove_member_list_between_ranks(self, min_rank: int, max_rank: int):
        return self.rdb.zremrangebyrank(self.main_key, min_rank, max_rank)

    def get_score(self, key: str) -> Number:
        return self.rdb.zscore(self.main_key, key)
