#!/usr/bin/env python
# coding=utf-8
import json


def read_json(fn: str):
    with open(fn) as fin:
        return json.loads((fin.read()))
