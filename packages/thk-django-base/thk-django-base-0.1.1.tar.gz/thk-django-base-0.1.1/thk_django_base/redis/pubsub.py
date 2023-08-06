# -*- coding: utf-8 -*-
import redis

from .base_on_connection import BaseOnConnection


class Publisher(BaseOnConnection):

    def __init__(self, channel_name: str, rdb: redis.Redis = None):
        super().__init__(rdb=rdb)
        self._channel_name = channel_name

    def publish(self, message: str) -> int:
        return self.rdb.publish(channel=self._channel_name, message=message)


class Subscriber(BaseOnConnection):

    def __init__(self, channel_name: str, rdb: redis.Redis = None):
        super().__init__(rdb=rdb)

        self._should_break = False
        self._subscriber = self.rdb.pubsub(ignore_subscribe_messages=True)
        self._channel_name = channel_name
        self._is_multi_channel = self._channel_name.find('*') >= 0

    def subscribe_channel(self):
        if self._is_multi_channel:
            self._subscriber.psubscribe(self._channel_name)
        else:
            self._subscriber.subscribe(self._channel_name)

    def unsubscribe_channel(self):
        if self._is_multi_channel:
            self._subscriber.punsubscribe(self._channel_name)
        else:
            self._subscriber.unsubscribe(self._channel_name)

    def start(self):
        self.subscribe_channel()
        self.run()
        self.unsubscribe_channel()

    def run(self):
        for message_dict in self._subscriber.listen():
            channel_name = message_dict.get('channel')
            message = message_dict.get('data')
            self.on_message(channel_name, message)
            if self._should_break:
                break

    def on_message(self, channel_name: str, message: str):
        raise NotImplementedError()
