import re


def to_camel_case(text):
    """Transform snake_case to CamelCase"""
    return re.sub(r"(_\w)", lambda x: x.group(1)[1:].upper(), text)


class NestedNamespace(object):
    # Limited javascript-like dot-notation access for testing module
    # Python special keywords (for,while,True, etc) not works
    def __init__(self, obj, **kwargs):
        super().__init__(**kwargs)
        self.__dict__["____original"] = obj

    def __getitem__(self, key):
        v = self.__dict__["____original"][key]
        return NestedNamespace(v) if isinstance(v, (dict, list)) else v

    def __setitem__(self, key, value):
        self.__dict__["____original"][key] = value

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __eq__(self, o):
        return self.__dict__["____original"].__eq__(o)

    def __ne__(self, o):
        return self.__dict__["____original"].__ne__(o)

    def __gt__(self, o):
        return self.__dict__["____original"].__gt__(o)

    def __lt__(self, o):
        return self.__dict__["____original"].__lt__(o)

    def __le__(self, o):
        return self.__dict__["____original"].__le__(o)

    def __ge__(self, o):
        return self.__dict__["____original"].__ge__(o)
