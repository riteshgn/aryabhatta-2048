import math
import random

from ai_utils import Singleton


DEFAULT_MAX_ENTRIES = 50000


class Cache(metaclass=Singleton):
    def __init__(self):
        self._records = {}
        self._metrics = {
            'total_reqs': 0,
            'hits': 0,
            'misses': 0,
            'record_count': 0
        }

    def has_key(self, key):
        return key in self._records

    def put(self, key, value):
        self._evict()
        self._metrics['record_count'] = self._metrics['record_count'] + 1
        self._records[key] = value

    def get(self, key):
        self._metrics['total_reqs'] = self._metrics['total_reqs'] + 1
        cache_value = self._records.get(key, None)
        if cache_value is None:
            self._metrics['misses'] = self._metrics['misses'] + 1
        else:
            self._metrics['hits'] = self._metrics['hits'] + 1
        return cache_value

    def metrics(self):
        return self._metrics

    def _evict(self):
        if self._metrics['record_count'] == DEFAULT_MAX_ENTRIES:
            random_int = math.floor(random.random() * self._metrics['record_count'])
            key_to_remove = list(self._records.keys())[random_int]
            if self._records.pop(key_to_remove, None) is not None:
                self._metrics['record_count'] = self._metrics['record_count'] - 1


