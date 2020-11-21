# junkdrawer
Useful Python utilities and patterns for a career Python developer.

## Utilities

### Log creator

Simple wrapper for creating Python logger instances with file handlers.

**Purpose**
- I frequently just need to initialize a logger with a handler to a file.
I didnt like having to rewrite all the handler init and config every time.
- Additionally, I made this utility able to also return "fangless" loggers in that it will return a logger with no filehandler, e.g. no logs will be produced other than possible terminal output. I found this really useful as many customers wanted scripts with the ability to toggle logging.

[code](/junkdrawer/log.py)

Usage
```python
# Create default logger.
#   - Default log level is found at log.DEFAULT_LOG_LEVEL.
#   - Default log file is found at log.DEFAULT_LOG_FP
>>> from log import get_logger
>>> log = get_file_logger()
>>> log.warning("Terminus")    # Will log to default log filepath with default log level mask.

# Create logger with arguments.
>>> log = get_file_logger(fp="path_to_log.log", log_level="DEBUG")
>>> log.info("It pays to be obvious when you are known for subtlety.")

# Create "fangless" logger. (see notes above on purpose)
>>> from log import get_logger
>>> log = get_file_logger(enabled=False)


# To change get_logger() defaults, just edit these global vars in log.py
DEFAULT_LOG_FP = "<program_name>.log"
DEFAULT_LOG_LEVEL = "WARNING"
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
