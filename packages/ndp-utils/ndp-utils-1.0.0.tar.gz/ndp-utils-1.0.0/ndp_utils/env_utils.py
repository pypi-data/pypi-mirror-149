import os

from typing import List, Dict, Union


def get_value(possible_value: List[str], env_vars: Dict[str, str] = None, default: str = None):
    env_vars = env_vars or dict(os.environ)
    for value in possible_value:
        res = env_vars.get(value)
        if res:
            return res
    return default


def is_true(any):
    # type: (Union[str, bool, int, None]) -> bool
    if not any or not isinstance(any, (str, bool, int)):
        return False
    return bool(any) and (str(any).isdigit() and bool(int(any))) or (str(any).capitalize() == str(True)) or False


def to_int(any):
    # type: (Union[str, bool, int, None]) -> int
    if not any or not isinstance(any, (str, bool, int)):
        return 0
    if isinstance(any, str):
        return any.isdigit() and int(any) or "." in any and int(float(any)) or 0
    return int(any)


def flat_map(f, xs):
    return [y for ys in xs for y in f(ys)]


def quote_if_needed(value):
    if isinstance(value, str):
        try:
            float(value)
            value = "'%s'" % value
        except ValueError:
            pass
    return value


def flat_dico(parent_keys, dico):
    result = []
    for key, value in dico.items():
        new_key = (*parent_keys, key)
        if isinstance(value, dict):
            result += flat_dico(parent_keys=new_key, dico=value)
        else:
            result.append((new_key, value))
    return result
