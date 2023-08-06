#!/usr/bin/env python
# coding=utf-8
import abc
import re
from typing import Dict, Tuple, List

from .handlerbase import Handler
from .keymatcher import KeyMatcher


def new_updater_from_dict(data: dict):
    if 'mapper' == data['class']:
        return MapperUpdater.from_dict(data)
    if 'regex' == data['class']:
        return RegexUpdater.from_dict(data)
    if 'combine' == data['class']:
        return CombineUpdater.from_dict(data)
    if 'format' == data['class']:
        return FormatUpdater.from_dict(data)


class Updater(Handler):
    """
    data updater，负责的工作是根据配置更新相应的字段
    负责处理具体的问题是:
    1、哪些字段需要更新
        1.1 字段确定： 静态确定，动态确定（需要根据值来确定）
        1.2 字段数目: 单个，多个
    2、怎么更新对应的字段
        2.1 静态依赖：只依赖自身的值
        2.2 动态依赖：其他字段的值

    """

    def __init__(self, key_matcher):
        self.key_matcher = key_matcher

    def iter_update_keys(self, item: Dict) -> Tuple[str, Dict]:
        """
        获取需要改动的key
        :param item: 被更新的对象
        :return: key which need to modify and data for updating value
        """
        if isinstance(self.key_matcher, dict):
            for key, value in self.key_matcher.items():
                yield key, {"value": value}
        else:
            for key, value in self.key_matcher.iter(item):
                yield key, value

    @abc.abstractmethod
    def get_new_value(self, item: Dict, key: str, options: Dict) -> object:
        """
        get new value for the specify key
        :param item: item
        :param key: field to update
        :param options:
        :return:
        """
        raise NotImplementedError('virtual function called')

    def log_empty_value(self, item, key):
        pass

    def handle(self, item: dict) -> dict:
        c = item.copy()
        for key, opt in self.iter_update_keys(item):
            value = self.get_new_value(item, key, opt)
            if value is None:
                self.log_empty_value(item, key)
                continue
            c[key] = value
        return c

    @staticmethod
    def form_matcher(matcher: Dict):
        if "class" not in matcher:
            return matcher["value"]
        return KeyMatcher.from_dict(matcher)

    @staticmethod
    def from_dict(data: dict):
        raise NotImplementedError('virtual function called')


class RegexUpdater(Updater):
    def __init__(self, key_matcher, pattern: str, field: str = None, flags=0, replace=""):
        Updater.__init__(self, key_matcher)
        self.regex = re.compile(pattern, flags=flags)
        self.field = field
        self.replace = replace

    def get_new_value(self, item: Dict, key: str, options: Dict) -> object:
        value = item.get(key if self.field is None else self.field)
        if value is None:
            return
        return self.regex.sub(self.replace, value)

    @staticmethod
    def from_dict(data: dict):
        matcher = RegexUpdater.form_matcher(data['key_matcher'])
        return RegexUpdater(matcher, data['pattern'], data.get('field'), data.get('flags', 0), data.get('replace', ''))


class CombineUpdater(Updater):
    def __init__(self, key_matcher, format_str: str, key: str, mapper: Dict[str, str]):
        Updater.__init__(self, key_matcher)
        self.format = format_str
        self.key = key
        self.mapper = mapper

    def get_new_value(self, item: Dict, key: str, options: Dict) -> object:
        # TODO: replace with secure formatting
        return self.format.format(**{"source": item[key], "dest": self.mapper.get(item[self.key])})

    @staticmethod
    def from_dict(data: dict):
        matcher = Updater.form_matcher(data['key_matcher'])
        return CombineUpdater(matcher, data['format'], data['key'], data['mapper'])


class FormatUpdater(Updater):
    def __init__(self, key_matcher, pattern: str, keys: List[str] = None):
        Updater.__init__(self, key_matcher)
        self.pattern = pattern
        self.keys = keys

    def get_new_value(self, item: Dict, key: str, options: Dict) -> object:
        # TODO: replace with secure formatting
        return self.pattern.format(**{k: item[k] for k in self.keys})

    @staticmethod
    def from_dict(data: dict):
        matcher = Updater.form_matcher(data['key_matcher'])
        return FormatUpdater(matcher, data['pattern'], data['keys'])


class MapperUpdater(Updater):
    """
    字典更新类，负责的工作是根据配置更新相应的字段
    负责处理具体的问题是:
    1、哪些字段需要更新
        1.1 字段确定： 静态确定，动态确定（需要根据值来确定）
        1.2 字段数目: 单个，多个
    2、怎么更新对应的字段
        2.1 静态依赖：只依赖自身的值
        2.2 动态依赖：其他字段的值

    """

    def __init__(self, key_matcher, key_dependence: Dict, value_maps: Dict):
        """

        :param key_matcher: key matcher, describe what keys to update or add
        :param key_dependence: describe how to get value from value_maps
        :param value_maps: value maps
        """
        Updater.__init__(self, key_matcher)
        self.key_dependence = key_dependence
        self.value_maps = value_maps

    def get_new_value_on_single_key(self, key, item: Dict, options: Dict):
        dep_key = self.key_dependence[key]['key']
        item_key = self.key_dependence[key].get('item_key', key)
        values = self.value_maps[dep_key]
        search_value = item[item_key] if self.key_dependence[key].get("type", "value") == "value" else item_key
        return values.get(search_value)

    def get_new_value_on_multiple_keys(self, keys, item: Dict, options: Dict):
        raise NotImplementedError('not implement yet')

    def get_new_value(self, item: Dict, key: str, options: Dict) -> object:
        """
        get new value for the specify key
        :param item: item
        :param key: field to update
        :param options:
        :return:
        """
        if key not in self.key_dependence:
            return options.get('value')
        if isinstance(self.key_dependence[key]['key'], str):
            return self.get_new_value_on_single_key(key, item, options)
        return self.get_new_value_on_multiple_keys(key, item, options)

    def log_empty_value(self, item, key):
        print(f"{item.get(key)} depends on key item[{key}]{self.key_dependence.get(key)} got None")

    @staticmethod
    def from_dict(data: dict):
        matcher = Updater.form_matcher(data['key_matcher'])
        return MapperUpdater(matcher, data['dependence'], data['value_maps'])
