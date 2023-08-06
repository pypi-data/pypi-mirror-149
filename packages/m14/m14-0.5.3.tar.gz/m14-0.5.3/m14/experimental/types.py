#!/usr/bin/env python3
# coding: utf-8

import dataclasses
from volkanic.compat import cached_property


def prefetch_cached_properties(obj):
    d = getattr(obj, '__dict__', {})
    for key, val in d.items():
        if isinstance(val, cached_property):
            getattr(obj, key)


class NovelDict(dict):
    def __getattr__(self, key: str):
        return self[key]

    def __setattr__(self, key: str, value):
        self[key] = value

    def __delattr__(self, key: str):
        del self[key]

    def get_properties(self) -> dict:
        props = {}
        for key, val in self.__class__.__dict__.items():
            if isinstance(val, (property, cached_property)):
                props[key] = getattr(self, key)
        return props

    def get_data_and_properties(self) -> dict:
        data = self.copy()
        data.update(self.get_properties())
        return data


@dataclasses.dataclass
class Record:
    @classmethod
    def from_dict(cls, dic: dict):
        names = set([f.name for f in dataclasses.fields(cls)])
        kwargs = {k: v for k, v in dic.items() if k in names}
        # noinspection PyArgumentList
        return cls(**kwargs)
