# -*- coding: utf-8 -*-
from .base_on_connection import BaseOnConnection


class ControlPanel(BaseOnConnection):

    def _get_info(self, section: str) -> dict:
        return self.rdb.info(section)

    @property
    def server_info(self) -> dict:
        return self._get_info('server')

    @property
    def client_info(self) -> dict:
        return self._get_info('clients')

    @property
    def memory_info(self) -> dict:
        return self._get_info('memory')

    @property
    def cpu_info(self) -> dict:
        return self._get_info('cpu')

    def flush_db(self) -> bool:
        return self.rdb.flushdb()

    def get_key_count(self) -> int:
        return self.rdb.dbsize()
