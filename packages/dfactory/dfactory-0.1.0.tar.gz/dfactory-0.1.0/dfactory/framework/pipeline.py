#!/usr/bin/env python
# coding=utf-8
from typing import List, Dict

from .handlerbase import Handler
from .common import new_operator_from_dict
from .seeders import Seeder


class Pipeline:

    def __init__(self):
        self.operators = []

    def handle(self, item):
        obj = item
        for c in self.operators:
            obj = c.handle(obj)
            if obj is None:
                break
        return obj

    def exit(self):
        for c in self.operators:
            if hasattr(c, 'on_exit'):
                c.on_exit()

    def enter(self):
        for c in self.operators:
            if hasattr(c, 'on_enter'):
                c.on_exit()

    def add(self, operator: Handler):
        self.operators.append(operator)

    def load_from_dict(self, data: List[Dict]):
        for c in data:
            obj = new_operator_from_dict(c)
            if obj is not None:
                self.add(obj)

    @staticmethod
    def from_dict(data: List[Dict]):
        p = Pipeline()
        p.load_from_dict(data)
        return p

    def iter(self, seeder: Seeder):
        for item in seeder.iter():
            if item is None:
                break
            obj = self.handle(item)
            if obj is None:
                continue
            yield obj

    def run(self, seeder: Seeder, fun=None):
        self.enter()
        for item in self.iter(seeder):
            if fun:
                fun(item)
        self.exit()
