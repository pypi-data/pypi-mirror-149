#!/usr/bin/env python
# coding=utf-8
import importlib

from .handlerbase import Handler
from .converters import new_converter_from_dict
from .writers import new_writer_from_dict

__config__ = {
    "converter": new_converter_from_dict,
    "writer": new_writer_from_dict
}


def import_module(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def new_operator_from_dict(data: dict):
    func = __config__.get(data['type'])
    if func is not None:
        return func(data)
    my_class = import_module(data["class"])
    if issubclass(my_class, Handler):
        if hasattr(my_class, 'from_dict'):
            return my_class.from_dict(data)
        return my_class()
