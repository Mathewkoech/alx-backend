#!/usr/bin/env python3
"""FIFO cache implementation"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache class implements a First-In-First-Out (FIFO) caching system.
    """
    def __init__(self):
        """
        Initialize the FIFOCache object.
        """
        super().__init__()
        self.keys = []

    def put(self, key, item):
        if key is not None and item is not None:
            if key in self.cache_data:
                self.keys.remove(key)
            self.cache_data[key] = item
            self.keys.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            removed_key = self.keys.pop(0)
            del self.cache_data[removed_key]
            print("DISCARD:", removed_key)

    def get(self, key):
        return self.cache_data.get(key, None)
