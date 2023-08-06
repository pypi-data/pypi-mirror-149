#!/usr/bin/env python
# coding=utf-8
import abc

from .handlerbase import Handler


def new_writer_from_dict(cfg: dict):
    if cfg['class'] == 'csv':
        return CsvWriter.from_dict(cfg)
    raise ValueError(f"unknown writer: {cfg['class']}")


class Writer(Handler):
    """
    基类
    将数据流写入文件或者数据库等等输出设备
    """

    def __enter__(self):
        self.on_create()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.on_destroy()

    @abc.abstractmethod
    def is_created(self) -> bool:
        raise NotImplementedError('virtual function called')

    @abc.abstractmethod
    def on_create(self):
        raise NotImplementedError('virtual function called')

    @abc.abstractmethod
    def on_destroy(self):
        raise NotImplementedError('virtual function called')

    @staticmethod
    def from_dict(data: dict):
        raise NotImplementedError('virtual function called')


class CsvWriter(Writer):
    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.file = None
        self.sep = kwargs.get('separator', ",")
        self.headers = kwargs.get('headers')
        self.keys = kwargs.get('keys')
        self.format = None

    def is_created(self) -> bool:
        return self.file is not None

    def on_create(self):
        try:
            self.file = open(self.fn, "w")
            self.prepare_format_fun()
            if self.headers is not None:
                self.file.write(self.sep.join(self.headers) + "\n")
        except IOError:
            pass

    def prepare_format_fun(self):
        if self.keys is not None:
            self.format = lambda a: self.sep.join([str(a[k]) for k in self.keys])
        else:
            self.format = lambda a: self.sep.join([str(a[k]) for k in a])

    def on_destroy(self):
        if self.file is not None:
            self.file.close()

    @staticmethod
    def from_dict(data: dict):
        kwargs = data.copy()
        kwargs.pop('key')
        return CsvWriter(data['path'], **kwargs)

    def handle(self, item: dict):
        try:
            self.file.write(self.format(item))
            self.file.write("\n")
        except IOError:
            pass
        return item
