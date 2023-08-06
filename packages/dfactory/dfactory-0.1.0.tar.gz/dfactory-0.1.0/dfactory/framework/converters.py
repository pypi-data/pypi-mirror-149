#!/usr/bin/env python
# coding=utf-8
from typing import List

from .handlerbase import Handler
from .matches import Match, new_match_from_dict
from .updaters import Updater, new_updater_from_dict
from ..utils.json import read_json


def new_converter_from_dict(data: dict):
    if data["class"] == "dict":
        return DictConverter.from_dict(data)
    return Converter.from_dict(data)


class Converter(Handler):

    def __init__(self, match: Match, updaters: List[Updater]):
        self.match = match
        self.updaters = updaters

    def handle(self, item: dict) -> dict:
        """
        converter，if match update data otherwise return the origin
        :param item: object to be handle
        :return:
        """
        if self.match.match(item):
            for u in self.updaters:
                item = u.handle(item)
        return item

    @staticmethod
    def from_dict(data):
        m = new_match_from_dict(data['match'])
        updaters = []
        if isinstance(data['updater'], dict):
            u = new_updater_from_dict(data['updater'])
            updaters.append(u)
        elif isinstance(data['updater'], list):
            for c in data['updater']:
                u = new_updater_from_dict(c)
                if u is not None:
                    updaters.append(u)
        return Converter(m, updaters)


class DictConverter(Handler):
    """
    convert one field of data with dict
    """

    def __init__(self, key: str, dst: str, mapper: dict = None):
        super(DictConverter, self).__init__()
        self.key = key
        self.dst = dst
        self.mapper = {} if mapper is None else mapper

    @staticmethod
    def from_dict(data: dict):
        mapper = data.get("mapper")
        if isinstance(mapper, str):
            mapper = read_json(mapper)
        return DictConverter(data['key'], data.get("dst", data["key"]), mapper)

    def handle(self, item: dict) -> dict:
        item[self.dst] = self.mapper.get(item[self.key], item[self.key])
        return item
