#!/usr/bin/env python3
# coding: utf-8

import base64
import collections
import dataclasses
import re
import typing
import urllib.parse


def url_to_filename(url):
    # http://stackoverflow.com/questions/295135/
    name = re.sub(r'[^\w\s_.-]+', '-', url)
    return re.sub(r'^{http|https|ftp}', '', name)


def validate_ipv4_address(address):
    import socket
    # http://stackoverflow.com/a/4017219/2925169
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True


def validate_ipv6_address(address):
    import socket
    # http://stackoverflow.com/a/4017219/2925169
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


@dataclasses.dataclass
class _URLMutable:
    _fields: typing.ClassVar = [
        'scheme', 'netloc', 'path',
        'params', 'query', 'fragment',
    ]
    scheme: str
    netloc: str
    path: str
    params: str
    query: dict
    fragment: str

    @classmethod
    def parse(cls, url: str):
        urlx = urllib.parse.urlparse(url)
        kwargs = {k: getattr(urlx, k) for k in cls._fields}
        query = dict(urllib.parse.parse_qsl(urlx.query))
        kwargs['query'] = query
        return cls(**kwargs)

    def __str__(self):
        dic = self.__dict__.copy()
        query = {str(k): str(v) for k, v in self.query.items()}
        dic['query'] = urllib.parse.urlencode(query)
        parts = [dic.get(k) for k in self._fields]
        return urllib.parse.urlunparse(parts)


class URLMutable(object):
    __slots__ = ['scheme', 'netloc', 'path', 'params', 'q', 'fragment']
    _fields = ['scheme', 'netloc', 'path', 'params', 'query', 'fragment']

    def __init__(self, url):
        pr = urllib.parse.urlparse(url)
        self.scheme = pr.scheme
        self.netloc = pr.netloc
        self.path = pr.path
        self.params = pr.params
        self.fragment = pr.fragment
        qsl = urllib.parse.parse_qsl(pr.query)
        self.q = collections.OrderedDict(qsl)

    @property
    def query(self):
        return urllib.parse.urlencode(self.q)

    @query.setter
    def query(self, value):
        qsl = urllib.parse.parse_qsl(value)
        self.q = collections.OrderedDict(qsl)

    def __getitem__(self, key):
        if key in self._fields:
            return getattr(self, key)
        raise KeyError(str(key))

    def __setitem__(self, key, value):
        if key in self._fields:
            return setattr(self, key, value)

    def __str__(self):
        values = [getattr(self, k) for k in self._fields]
        return urllib.parse.urlunparse(values)

    def __repr__(self):
        cn = self.__class__.__name__
        return '{}({})'.format(cn, repr(str(self)))

    def embed_link(self, key, guest_url, safe=True, func=None):
        """
        :param key:
        :param guest_url:
        :param safe: avoid chaining embedment
        :param func: process resulting base64 string with this func
        :return: a LinkMutable instance
        """
        # firstly, remove that key in guest_url!
        if safe:
            guest_urlmut = URLMutable(guest_url)
            if key in guest_urlmut.q:
                guest_urlmut.q.pop(key)
                guest_url = str(guest_urlmut)

        guest = base64.urlsafe_b64encode(guest_url.encode('utf-8'))
        guest = guest.decode('utf-8')
        guest = guest.replace('=', '').strip()
        if func:
            guest = func(guest)
        self.q[key] = guest

    def unembed_link(self, key, func=None, remove=True):
        if key not in self.q:
            return ''
        if remove:
            em = self.q.pop(key)
        else:
            em = self.q.get(key)
        if func:
            em = func(em)
        em += '=' * ((4 - len(em) % 4) % 4)
        em = em.encode('ascii')
        try:
            return base64.urlsafe_b64decode(em).decode('utf-8')
        except Exception:
            return ''


def url_simplify(url, queries=('id',)):
    queries = set(queries)
    mut = URLMutable(url)
    q = [kv for kv in mut.q.items() if kv[0] in queries]
    mut.q = collections.OrderedDict(q)
    mut['fragment'] = ''
    return mut


def run_urlsim(prog, args, func=None):
    import argparse
    func = url_simplify if func is None else func
    desc = 'simplify a url'
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    parser.add_argument('-q', '--quote', action='store_true')
    parser.add_argument('url')
    parser.add_argument('query', nargs='*')
    ns = parser.parse_args(args)
    url = str(func(ns.url, ns.query))
    if ns.quote:
        import shlex
        url = shlex.quote(url)
    print(url)
