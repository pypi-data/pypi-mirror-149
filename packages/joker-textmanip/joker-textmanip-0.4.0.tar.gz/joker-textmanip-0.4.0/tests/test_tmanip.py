#!/usr/bin/env python3
# coding: utf-8

from joker.textmanip import random_hex, random_string


def test_random():
    for n in range(10):
        assert len(random_hex(n)) == n
        assert len(random_string(n)) == n
