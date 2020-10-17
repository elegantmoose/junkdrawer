# junkdrawer
Useful Python utilities and patterns for a career python developer.

## Utilities

### Log creator

Simple wrapper for creating Python logger instances with file handlers.

[code](/junkdrawer/log.py)

Usage
```
(TODO)
```

### Compare Storage Perfomance of Python Data Structures

Evaluate the performance of the following data structures for a data object:
  - dict
  - list
  - dataclass
  - slots

[code](junkdrawer/dict_vs_list_vs_dataclass_vs_slots.py)

Usage:
```
TODO
```

### Nested dictionary and list access

_(not coded by maintainer, see module docstrings for reference)_

Utility functions for nested dictionary and list access.

[code](junkdrawer/nested_dict_access_by_key_list.py)

Usage:
```sh
TODO
```

### JSON/Dict-like data filter

A filter function that can work on any JSON-like data structure (i.e. lists, dicts, and values). The filter function takes a list of the JSON-like data instances and then applies filters (specified by simple filter format) to them. Filters can be supplied to filter out matching instances or filter in matching instances. The filters can be for string matches, substring check (via python "in"), re.search pattern or re.match pattern. Filters may also be flagged to be applied separately as a set (i.e. compound filter).

[code](/junkdrawer/json_data_struct_filter.py)

Usage
```
(TODO)
```

### Class/Function input/output monitor

Wrap classes and functions to record all input and output.

[code](junkdrawer/func_io_monitor.py)

Usage
```sh
>>from func_io_monitor import func_io_monitor, class_io_monitor, RECORD_TYPES
>>
>># EXAMPLE: Single Function
>># For this example we want to monitor a single function called 'add'
>>
>>def add(x,y)
>>    return x + y
>>
>># This creates a monitor for 'add()' that will record all input/output to 'add()' in JSON format
>># to a file named "add_monitor.json"
>>add_monitor = func_io_monitor(add, record_type=RECORD_TYPES.json, record_fp="add_monitor.json")
>
>># Now use 'add_monitor' as you would 'add()'
>>add_monitor(1,2)
>>3
>>
>># In 'add_monitor.json', you will see:
>># {"__main__.<none>.add": [{"time": 1597074458.0931141, "in": {"args": [1, 2], "kwargs": {}}, "out": "3"}]}
>>
>>
>># EXAMPLE: Entire Class instance
>>
>> # In this case, we want to monitor the entire class instance, i.e. all its methods
>>class arith():
>>    def __init__(self):
>>        self.t = "test"
>>    def add(self, x, y):
>>        return x + y
>>    def del_(self, x, y):
>>        return x - y 
>>
>>a = arith()
>>
>># Creates a monitor for class methods of instance, that will record all inputs/outputs
>># in python logging format the log file "arith.log"
>>arith_monitor = class_io_monitor(a, record_fp="arith.log", record_type=RECORD_TYPES.log)
>>arith_monitor.add(1,2)
>>3
>>arith_monitor.del_(0, -2)
>>-2
>>
>># In "arith.log", you will see:
>>#2020-08-10 12:05:26 INFO     __main__.arith.add - IN: {'args': (1, 2), 'kwargs': {}} - OUT: 3 
>>#
>>#2020-08-10 12:05:26 INFO     __main__.arith.del_ - IN: {'args': (0, -2), 'kwargs': {}} - OUT: 2
>>
"""
```
