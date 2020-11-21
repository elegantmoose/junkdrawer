"""
--- Purpose
Compare data structure storage performance of:
  - dict
  - list
  - dataclasses
  - slots
  
--- Usage
First, create a simple object data model in a yaml file.

Supported primary types are:
    - str
    - int
    - float
    - complex
    - bool
    - list
    - tuple
    - set
    - dict

Supported item types (e.g. the subtype used for when the primay type
is one of [list, tuple, set, dict].
    - int
    - float
    - bool

Data Model File (yaml)
```
var1: int
var2: bool
var3: str
var4: float
var5: complex
var6: list:int
var7: tuple:bool
var8: set:float
var9: dict:int
```


>>python dict_vs_list_vs_dataclass_vs_slots.py -d <yaml data file> -n <n instances>
"""

import argparse
from dataclasses import dataclass, make_dataclass
from enum import Enum
from pympler import asizeof
import random
import uuid
from yaml import safe_load


STRING = "It is not the critic who counts; not the man who points out how the strong man stumbles, or where the doer of deeds could have done them better. The credit belongs to the man who is actually in the arena, whose face is marred by dust and sweat and blood; who strives valiantly; who errs, who comes short again and again, because there is no effort without error and shortcoming; but who does actually strive to do the deeds; who knows great enthusiasms, the great devotions; who spends himself in a worthy cause; who at the best knows in the end the triumph of high achievement, and who at the worst, if he fails, at least fails while daring greatly, so that his place shall never be with those cold and timid souls who neither know victory nor defeat."
STRING_SIZE = 10
INT_RANGE = (0,10000000)
FLOAT_RANGE = (0, 1000000)
TUPLE_SIZE = 10
LIST_SIZE = 10
DICT_SIZE = 10
SET_SIZE = 10


class TYPES(Enum):
    STR = str
    BOOL = bool
    INT = int
    FLOAT = float
    COMPLEX = complex
    LIST = list
    TUPLE = tuple
    DICT = dict
    SET = set


class ITEM_TYPES(Enum):
    BOOL = bool
    INT = int
    FLOAT = float


def _random_item_values(item_type, size):
    """
    NOTE: no checking of item_type, assumes is one of ITEM_TYPES
    """
    if item_type == ITEM_TYPES.INT:
        l = [random.randint(INT_RANGE[0], INT_RANGE[1]) for i in range(size)]
    elif item_type == ITEM_TYPES.BOOL:
        l = [random.choice([True, False]) for i in range(size)]
    elif item_type == ITEM_TYPES.FLOAT:
        l = [random.uniform(FLOAT_RANGE[0], FLOAT_RANGE[1]) for i in range(size)]
    else:
        raise ValueError(f"Item type {item_type} not supported.")
    return l


def _check_and_get_types(type_str):
    """ """
    if ":" in type_str:
        primary_type, item_type  = type_str.split(":")
    else:
        primary_type = type_str
        item_type = None
    try:
        primary_type = getattr(TYPES, primary_type.upper())
    except ValueError:
        raise Warning(f"Data field type {primary_type} is not supported as a primary field type.")
        primary_type = None
    if item_type:
        try:
            item_type = getattr(ITEM_TYPES, item_type.upper())
        except ValueError:
            raise Warning(f"Data field type {item_type} is not supported as a item field type.")
    return primary_type, item_type


def _random_data_fields(data_model):
    """

    Args:
        data_model(dict): data field names and types

    Returns: (dict)
    """
    fields_values = {}
    for name, type_ in data_model.items():
        primary_type, item_type = _check_and_get_types(type_)
        if not primary_type:
            continue

        if primary_type == TYPES.STR:
            v = STRING[0:STRING_SIZE]
        elif primary_type == TYPES.INT:
            v = random.randint(INT_RANGE[0], INT_RANGE[1])
        elif primary_type == TYPES.BOOL:
            v = random.choice([True, False])
        elif primary_type == TYPES.FLOAT:
            v = random.uniform(FLOAT_RANGE[0], FLOAT_RANGE[1])
        elif primary_type == TYPES.COMPLEX:
            v = TYPES.COMPLEX.value(
                random.randint(INT_RANGE[0], INT_RANGE[1]), 
                random.randint(INT_RANGE[0], INT_RANGE[1]))
        elif primary_type == TYPES.LIST:
            v = TYPES.LIST.value(_random_item_values(item_type, LIST_SIZE))
        elif primary_type == TYPES.TUPLE:
            v = TYPES.TUPLE.value(_random_item_values(item_type, TUPLE_SIZE))
        elif primary_type == TYPES.SET:
            v = TYPES.SET.value(_random_item_values(item_type, SET_SIZE))
        elif primary_type == TYPES.DICT:
            v = {i: item_type for i in range(DICT_SIZE)}

        fields_values[name] = v

    return fields_values


def _get_argparser():
    """to organize and clean format argparser args"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--data-model",
        action="store",
        dest="data_model",
        required=True,
        help="yaml file of data model to use"
    )

    parser.add_argument(
        "-n",
        action="store",
        dest="n",
        default=10000,
        help="count of data structures to create"
    )
    return parser
    
    
def main():
    parser = _get_argparser()

    # parse all args and put in dict
    args = vars(parser.parse_args())
    args["n"] = int(args["n"])

    data_model = safe_load(open(args["data_model"], 'r'))
    DataClass = make_dataclass("MK", data_model)
    SlotsClass =  type("MKS", (object, ), {"__slots__": list(data_model.keys())})

    dicts = []
    lists = []
    slots = []
    data_classes = []
    for _ in range(args['n']):
        fields_values = _random_data_fields(data_model)
        dicts.append(fields_values)
        lists.append(list(fields_values.values()))
        data_classes.append(DataClass(**fields_values))
        sc = SlotsClass()
        for k,v in fields_values.items():
            setattr(sc, k, v)
        slots.append(sc)

    print(f"n is {args['n']}")
    print(f"Size of data classes: {asizeof.asizeof(data_classes)} bytes")
    print(f"Size of slots classes: {asizeof.asizeof(slots)} bytes")
    print(f"Size of lists: {asizeof.asizeof(lists)} bytes")
    print(f"Size of dicts: {asizeof.asizeof(dicts)} bytes")


if __name__ == "__main__":
    main()
