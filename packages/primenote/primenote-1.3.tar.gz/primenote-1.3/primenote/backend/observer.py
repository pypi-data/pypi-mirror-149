#!/usr/bin/python3
from typing import Callable


def callback(func: Callable) -> Callable:
    """Attaches a callback hook prior to function call"""

    def wrapper(self, *args, **kwargs) -> Callable:
        self.cb()
        return func(self, *args, **kwargs)

    return wrapper


class Observer(dict):
    """Dict object which emits a callback signal when its content, or its subitem content is modified"""

    def __init__(self, *args, callback: Callable):
        super().__init__(*args)
        self.cb = callback

    @callback
    def __delitem__(self, *args):
        super().__delitem__(*args)

    @callback
    def __setitem__(self, key: any, value: any):
        """Fires a callback function when a value is changed"""
        value = self._replace(value)
        super().__setitem__(key, value)
        if isinstance(value, dict):
            self._convert(value)

    def _convert(self, dct: dict):
        """Recursively converts nested dict to Observer subclasses"""
        for key, value in dct.items():
            dct[key] = self._replace(value)
            if isinstance(value, dict):
                self._convert(value)

    def _replace(self, obj: any) -> any:
        """Converts data structures to Observer subclasses"""
        obj = Observer(obj, callback=self.cb) if isinstance(obj, dict) else obj
        obj = ObserverSet(obj, callback=self.cb) if isinstance(obj, set) else obj
        obj = ObserverList(obj, callback=self.cb) if isinstance(obj, list) else obj
        return obj

    @callback
    def clear(self):
        super().clear()

    @callback
    def pop(self, *args) -> any:
        return super().pop(*args)

    @callback
    def popitem(self) -> any:
        return super().popitem()

    @callback
    def setdefault(self, *args) -> any:
        value = super().setdefault(*args)
        self._convert(self)
        return value

    @callback
    def update(self, *args):
        super().update(*args)
        self._convert(self)


class ObserverList(list):
    """List object which emits a callback signal when its content is modified"""

    def __init__(self, *args, callback: Callable):
        super().__init__(*args)
        self.cb = callback

    @callback
    def __delitem__(self, *args):
        super().__delitem__(*args)

    @callback
    def __iadd__(self, *args) -> list:
        return super().__iadd__(*args)

    @callback
    def __setitem__(self, *args):
        super().__setitem__(*args)

    @callback
    def append(self, *args):
        super().append(*args)

    @callback
    def clear(self):
        super().clear()

    @callback
    def extend(self, *args):
        super().extend(*args)

    @callback
    def insert(self, *args):
        super().insert(*args)

    @callback
    def pop(self, *args) -> any:
        return super().pop(*args)

    @callback
    def remove(self, *args):
        super().remove(*args)

    @callback
    def reverse(self):
        super().reverse()

    @callback
    def sort(self, *args, **kwargs):
        super().sort(*args, **kwargs)


class ObserverSet(set):
    """Set object which emits a callback signal when its content is modified"""

    def __init__(self, *args, callback: Callable):
        super().__init__(*args)
        self.cb = callback

    @callback
    def __iand__(self, *args) -> set:
        return super().__iand__(*args)

    @callback
    def __ior__(self, *args) -> set:
        return super().__ror__(*args)

    @callback
    def __isub__(self, *args) -> set:
        return super().__isub__(*args)

    @callback
    def __ixor__(self, *args) -> set:
        return super().__ixor__(*args)

    @callback
    def add(self, *args):
        super().add(*args)

    @callback
    def clear(self):
        super().clear()

    @callback
    def difference_update(self, *args):
        super().difference_update(*args)

    @callback
    def discard(self, *args):
        super().discard(*args)

    @callback
    def intersection_update(self, *args):
        super().intersection_update(*args)

    @callback
    def pop(self) -> any:
        return super().pop()

    @callback
    def remove(self, *args):
        super().remove(*args)

    @callback
    def symmetric_difference_update(self, *args):
        super().symmetric_difference_update(*args)

    @callback
    def update(self, *args):
        super().update(*args)
