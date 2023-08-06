#!/usr/bin/env python3
# coding: utf-8

from joker.textmanip import charset


def test():
    print(
        charset.get_all_encodings(),
        charset.get_most_frequent_characters(),
        charset.get_unicode_blocks(),
        sep='\n'
    )


if __name__ == '__main__':
    test()