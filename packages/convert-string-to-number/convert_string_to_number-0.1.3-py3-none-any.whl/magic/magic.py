#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import numpy as np

# there are a number of hashing functions you can pick, and they provide tags of different lengths and security levels.
hashing_func = hashlib.md5

# the lambda func does three things
# 1. hash a given string using the given algorithm
# 2. retrive its hex hash tag
# 3. convert hex to integer
str2int = lambda s: int(hashing_func(s.encode()).hexdigest(), 16)


class MagicString:
    def str2number(self, source: str, size=99_999_999_999):
        if not source or source is None:
            raise ValueError("Thiếu thông tin đầu vào")

        source_length = len(source)
        delta = 1
        total = 0

        for i in range(source_length):
            if i % 4 == 0:
                delta = 1
            else:
                delta = delta * 256
            total += ord(source[i]) * delta
        return total % size

    def str2int(self, source: str, size=99_999_999_999):
        if not source or source is None:
            raise ValueError("Thiếu thông tin đầu vào")

        return str2int(source) % size


magic_str = MagicString()
