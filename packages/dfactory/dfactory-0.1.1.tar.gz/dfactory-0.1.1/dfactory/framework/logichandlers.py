#!/usr/bin/env python
# coding=utf-8
# !/usr/bin/env python
# coding=utf-8
from .handlerbase import Handler
from .common import new_operator_from_dict


class LinkHandler(Handler):
    """
    LinkHandler
    a group of handler
    run in sequence until one success
    """

    def __init__(self):
        super().__init__()
        self.handlers = []
        self.matches = {}

    def check(self, item):
        for k, v in self.matches.items():
            keys = k.split(".")
            obj = item
            for key in keys:
                obj = obj.get(key)
                if obj is None:
                    return False
            if obj != v:
                return False
        return True

    def handle(self, item: dict) -> dict:
        for h in self.handlers:
            obj = h.handle(item)
            if self.check(obj):
                return obj
        return item

    @staticmethod
    def from_dict(data):
        h = LinkHandler()
        h.matches = data["match"]
        for item in data["handlers"]:
            handler = new_operator_from_dict(item)
            if handler is not None:
                h.handlers.append(handler)
        return h
