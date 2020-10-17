"""Handles both nested dictionary and list access

Source: https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys
"""

from functools import reduce  # forward compatibility for Python3
import operator


def get_by_path(root, items):
    """Access a nested object in root by item sequence"""
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence"""
    get_by_path(root, items[:-1])[items[-1]] = value


def in_nested_path(root, items):
    """ 'in' equivalent for a nested dict/list structure"""
    try:
        get_by_path(root, items)
    except KeyError:
        return False

    return True
