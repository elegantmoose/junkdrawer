"""Handles both nested dictionary and list access

Source: https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys

Usage --

```
from nested_dict_access_by_key_list import get_by_path, set_by_path, in_nested_path

# retrieve nested dict item
>>> d = {"1": {"2":{"3": "salvador"}}} 
>>> get_by_path(d, ["1", "2", "3"])
'salvador'

# Note that nested retrieval may be dynamic
>>> d = {"1": {"2":{"3": "salvador"}}} 
>>> level_2 = "2"
>>> get_by_path(d, ["1", level_2, "3"])
'salvador'

# Note how nested lists are navigated
>>> d
{'1': {'2': {'3': ['seldon', {'4': 'mallow'}]}}}
>>> get_by_path(d, ["1", "2", "3", 1, "4"])
'mallow'

# set nested dict item (note: can also be done dynamically with variables)
>>> d
{'1': {'2': {'3': 'salvador'}}}
>>> set_by_path(d, ["1", "2"], "mallow")
>>> d
{'1': {'2': 'mallow'}}
```

# Use Python "in" operator on nested dict/list
#
# Note how lists are navigated here. We navigate to dict with
# key '3', then jump to index 1, then back to key "4
>>> d
{'1': {'2': {'3': ['seldon', {'4': 'mallow'}]}}}
>>> in_nested_path(d, ["1", "2", "3", 1, "4"])
True
```

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
