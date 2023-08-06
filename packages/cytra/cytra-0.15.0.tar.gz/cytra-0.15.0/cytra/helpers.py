import re


def to_camel_case(text):
    """Transform snake_case to CamelCase"""
    return re.sub(r"(_\w)", lambda x: x.group(1)[1:].upper(), text)


def dot_object(obj):
    # Limited javascript-like dot-notation access for testing module
    # Python special keywords (for,while,True, etc) not works

    if isinstance(obj, dict):
        return DotDict(obj)

    if isinstance(obj, list):
        return DotList(obj)

    return obj


class DotList(list):
    def __getitem__(self, key):
        return dot_object(super().__getitem__(key))


class DotDict(dict):
    def __getitem__(self, key):
        return dot_object(super().__getitem__(key))

    def get(self, key, default=None):
        return dot_object(super().get(key, default))

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
