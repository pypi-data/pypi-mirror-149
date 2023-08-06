#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib

# there are a number of hashing functions you can pick, and they provide tags of different lengths and security levels.
hashing_func = hashlib.md5

# the lambda func does three things
# 1. hash a given string using the given algorithm
# 2. retrive its hex hash tag
# 3. convert hex to integer
str2int = lambda s: int(hashing_func(s.encode()).hexdigest(), 16)


class Magic:
    def __init__(self, source=None, size=99_999_999_999):
        self.source = source
        self.size = size
        self.hash_number = None

    def set_source(self, source):
        self.source = source

    def set_max_size(self, size):
        self.size = size

    def convert2Int(self):
        if self.source is None:
            raise ValueError("source is required")

        source_hash = str2int(self.source)
        self.hash_number = source_hash % self.size
        return self.hash_number

    def get_hash_number(self):
        return self.hash_number

    def get_source(self):
        return self.source

    def get_size(self):
        return self.size
