#!/usr/bin/env python
# coding=utf-8
import abc


class Handler(object):

    @abc.abstractmethod
    def handle(self, item: dict) -> dict:
        raise NotImplementedError("virtual function called")


class CondHandler(Handler):

    @abc.abstractmethod
    def check(self, item: dict) -> bool:
        raise NotImplementedError('virtual function called')

    @abc.abstractmethod
    def operate(self, item: dict) -> dict:
        raise NotImplementedError('virtual function called')

    def handle(self, item: dict) -> dict:
        if self.check(item):
            return self.operate(item)
        return item
