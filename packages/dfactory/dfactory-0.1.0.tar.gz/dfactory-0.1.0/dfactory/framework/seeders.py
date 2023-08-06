#!/usr/bin/env python
# coding=utf-8
from typing import List


class Seeder:

    def iter(self) -> dict:
        raise NotImplementedError('virtual function called')


class CsvSeeder(Seeder):
    """
    a seeder that generate dict item from csv file line by line
    """

    def __init__(self, fn: str, keys: List[str], sep=","):
        self.fn = fn
        self._reader = None
        self.sep = sep
        self.keys = keys

    def iter(self):
        with self:
            for line in self._reader:
                item = self.line2item(line.strip())
                if item is None:
                    continue
                yield item

    def line2item(self, line: str):
        parts = line.split(self.sep, maxsplit=len(self.keys))
        if len(parts) != len(self.keys):
            return
        return {self.keys[k]: parts[k] for k in range(len(self.keys))}

    def close(self):
        if self._reader is not None:
            self._reader.close()
        self._reader = None

    def __enter__(self):
        if self._reader is None:
            self._reader = open(self.fn)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def from_dict(data: dict):
        return CsvSeeder(data['src'], data['keys'], data.get('sep', ','))
