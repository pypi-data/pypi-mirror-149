try:
    import ujson as json
except ImportError:
    import json


def is_float_num(str):
    s = str.split(".")
    if len(s) != 2:
        return False
    else:
        for si in s:
            if not si.isdigit():
                return False
        return True
