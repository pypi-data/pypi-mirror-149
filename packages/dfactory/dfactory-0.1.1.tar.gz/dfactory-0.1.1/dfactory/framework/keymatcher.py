#!/usr/bin/env python
# coding=utf-8
import abc
import re
from typing import Dict, List


class KeyMatcher:

    @abc.abstractmethod
    def iter(self, item: Dict):
        raise NotImplementedError("virtual function called")

    @staticmethod
    def from_dict(data):
        cls = __class_map__.get(data.get('class'))
        if cls is not None:
            return cls.from_dict(data)


class ListKeyMatcher(KeyMatcher):
    def __init__(self, keys: List[str]):
        self.keys = keys

    def iter(self, item: Dict):
        for key in self.keys:
            yield key, None

    @staticmethod
    def from_dict(data):
        return ListKeyMatcher(data['keys'])


class RegexKeyMatcher(KeyMatcher):
    def __init__(self, regex: str):
        self.pattern = re.compile(regex)

    def iter(self, item: Dict):
        for key in item.keys():
            if self.pattern.match(key):
                yield key, None

    @staticmethod
    def from_dict(data):
        return RegexKeyMatcher(data['regex'])


class FormatKeyMatcher(KeyMatcher):
    def __init__(self, format_str: str, keys: List[str]):
        self.format_str = format_str
        self.keys = keys

    def iter(self, item: Dict):
        yield self.format_str.format(**{k: item[k] for k in self.keys}), None

    @staticmethod
    def from_dict(data):
        return FormatKeyMatcher(data['format'], data["keys"])


__class_map__ = {
    "list": ListKeyMatcher,
    "regex": RegexKeyMatcher,
    "format": FormatKeyMatcher,
}
