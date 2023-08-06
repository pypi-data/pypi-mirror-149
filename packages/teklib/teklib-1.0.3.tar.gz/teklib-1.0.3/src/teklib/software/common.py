# -*- coding: utf-8 -*-
"""
 Common Files
"""


class Record(object):
    """ A record class that allows you to automatically
    generate a structure based on strings.
    """

    def __init__(self, name):
        self.name = name

    def setattr(self, name, value):
        parts = name.split(".")
        obj = self
        for attr in parts[:-1]:
            if hasattr(obj, attr):
                obj = getattr(obj, attr)
                if not isinstance(obj, Record):
                    raise AttributeError
            else:
                setattr(obj, attr, Record(attr))
                obj = getattr(obj, attr)
        setattr(obj, parts[-1], value)

    def addattr(self, **kwargs):
        for k, v in kwargs.items():
            self.setattr(k, v)
