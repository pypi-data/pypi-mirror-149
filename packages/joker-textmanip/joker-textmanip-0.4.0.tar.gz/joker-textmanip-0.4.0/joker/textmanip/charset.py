#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import functools
import re

from joker.cast import cache_lookup
from volkanic.utils import under_package_dir

import joker.textmanip

thin_space = '\u2009'
zero_width_space = '\u200b'
ideographic_space = '\u3000'

# https://www.compart.com/en/unicode/block/U+2600
_music_notes = '\u2669\u266a\u266b\u266c'

_const_cache = {}


def _read_lines(path):
    lines = (lx.strip() for lx in open(path))
    return [lx for lx in lines if lx]


def const_getter(func):
    return functools.wraps(func)(
        lambda: cache_lookup(_const_cache, func, func)
    )


def const_lookup(func):
    return functools.wraps(func)(
        lambda *args: cache_lookup(_const_cache, (func, args), func, *args)
    )


def _locate(name):
    return under_package_dir(joker.textmanip, 'data', name)


@const_getter
def get_unicode_blocks():
    path = _locate('unicode_blocks.txt')
    results = []
    for line in _read_lines(path):
        head, tail, title = line.split(None, 2)
        head = int(head, base=0)
        tail = int(tail, base=0)
        results.append((head, tail, title))


def search_unicode_blocks(pattern):
    regex = re.compile(pattern)
    blocks = []
    for tup in get_unicode_blocks():
        if regex.search(tup[2]):
            blocks.append(tup)
    return blocks


def blocks_to_name_tuple_map(blocks=None):
    if blocks is None:
        blocks = get_unicode_blocks()
    return {tu[2]: tuple(tu[:2]) for tu in blocks}


@const_getter
def get_all_encodings():
    return _read_lines(_locate('encodings.txt'))


@const_lookup
def get_most_frequent_characters(lang='sc'):
    path = 'data/mfc-{}.txt'.format(lang)
    path = under_package_dir(joker.textmanip, path)
    return ''.join(_read_lines(path))


# https://unicode-table.com/en/sets/roman-numerals/
roman_numerals = {
    1: 'Ⅰ',
    2: 'Ⅱ',
    3: 'Ⅲ',
    4: 'Ⅳ',
    5: 'Ⅴ',
    6: 'Ⅵ',
    7: 'Ⅶ',
    8: 'Ⅷ',
    9: 'Ⅸ',
    10: 'Ⅹ',
    11: 'Ⅺ',
    12: 'Ⅻ',
}

small_roman_numerals = {
    1: 'ⅰ',
    2: 'ⅱ',
    3: 'ⅲ',
    4: 'ⅳ',
    5: 'ⅴ',
    6: 'ⅵ',
    7: 'ⅶ',
    8: 'ⅷ',
    9: 'ⅸ',
    10: 'ⅹ',
    11: 'ⅺ',
    12: 'ⅻ'
}
