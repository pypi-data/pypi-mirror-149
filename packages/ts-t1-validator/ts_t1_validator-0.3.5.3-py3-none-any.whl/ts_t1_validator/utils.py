import math


def is_number(s):
    try:
        i = float(s)
        if math.isnan(i):
            raise ValueError

        return True
    except (ValueError, TypeError):
        return False


def is_int(v) -> bool:
    """
    we assume that int we can define real integer or numbers with .0 decimals
    :param v: mixed
    :return: bool
    """
    # return type(v) is int or math.modf(v)[0] == 0
    return isinstance(v, int)


def is_bool(v):
    """
    check that value is bool

    :param v:
    :return: bool
    """
    return type(v) is bool or v.lower() in ("true", "false", "1", "0")


def str2bool(v: str):
    """
    convert str to boolean
    :param v: str
    :return: bool
    """
    if type(v) is bool:
        return v is True
    else:
        return v.lower() in ("true", "1")
