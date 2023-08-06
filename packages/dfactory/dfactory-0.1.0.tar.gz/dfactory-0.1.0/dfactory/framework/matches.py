#!/usr/bin/env python
# coding=utf-8
import abc
import re


def new_match_from_dict(data: dict):
    if data["class"] == "or":
        return OrMatch.from_dict(data)
    elif data['class'] == "and":
        return AndMatch.from_dict(data)
    elif data['class'] == 'key':
        return KeyMatch.from_dict(data)
    elif data['class'] == 'regex':
        return RegexMatch.from_dict(data)
    elif data['class'] == 'true':
        return TrueMatch.from_dict(data)
    elif data['class'] == 'not':
        return NotMatch.from_dict(data)


class Match(object):
    @abc.abstractmethod
    def match(self, item: dict):
        raise NotImplementedError('virtual function called')

    @staticmethod
    def from_dict(data: dict):
        raise NotImplementedError('virtual function called')


class KeyMatch(Match):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def match(self, item: dict):
        if isinstance(self.value, list):
            return item.get(self.key) in self.value
        return item.get(self.key) == self.value

    @staticmethod
    def from_dict(data: dict):
        return KeyMatch(data["key"], data["value"])


class TrueMatch(Match):

    def match(self, item: dict):
        return True

    @staticmethod
    def from_dict(data: dict):
        return TrueMatch()


class RegexMatch(Match):
    def __init__(self, key, pattern, flag=0):
        self.key = key
        self.pattern = None
        if isinstance(pattern, str):
            self.pattern = re.compile(pattern, flag)
        elif isinstance(pattern, re.Pattern):
            self.pattern = pattern
        else:
            raise ValueError("invalid pattern type, only str or re.Pattern allowed")

    def match(self, item: dict):
        return self.pattern.match(item.get(self.key))

    @staticmethod
    def from_dict(data: dict):
        return RegexMatch(data["key"], data["value"], data.get('flag', 0))


class AndMatch(Match):
    def __init__(self, a: Match, b: Match):
        self.a = a
        self.b = b

    def match(self, item: dict):
        return self.a.match(item) and self.b.match(item)

    @staticmethod
    def from_dict(data: dict):
        a, b = new_match_from_dict(data['a']), new_match_from_dict(data['b'])
        if a is None or b is None:
            raise ValueError('None type Match')
        return AndMatch(a, b)


class OrMatch(Match):
    def __init__(self, a: Match, b: Match):
        self.a = a
        self.b = b

    def match(self, item: dict):
        return self.a.match(item) or self.b.match(item)

    @staticmethod
    def from_dict(data: dict):
        a, b = new_match_from_dict(data['a']), new_match_from_dict(data['b'])
        if a is None or b is None:
            raise ValueError('None type Match')
        return OrMatch(a, b)


class NotMatch(Match):
    def __init__(self, a: Match):
        self.a = a

    def match(self, item: dict):
        return not self.a.match(item)

    @staticmethod
    def from_dict(data: dict):
        a = new_match_from_dict(data['match'])
        if a is None:
            raise ValueError('None type Match')
        return NotMatch(a)
