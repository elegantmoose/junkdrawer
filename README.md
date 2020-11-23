# junkdrawer
Useful Python utilities and patterns for a career Python developer.

## Install

From PyPi
```sh
pip install junkdrawer
```

From Github
```sh
git clone git@github.com:elegantmoose/junkdrawer.git
cd junkdrawer
pip install .
```

## Utilities

**Contents**  

1. [ArgumentParser Pattern](#1-ArgumentParser-Pattern)  
2. [File Log Creator](#2-File-Log-Creator)
3. [Compare Storage Perfomance of Python Data Structures](#3-Compare-Storage-Perfomance-of-Python-Data-Structures)
4. [JSON-like data filter](#4-JSON-like-data-filter)
5. [Nested dictionary and list access](#5-Nested-dictionary-and-list-access)
6. [Class-Function IO Monitor](#6-Class-Function-IO-Monitor)
7. [Flask App Skeleton](#7-Flask-App-Skeleton)

### 1. ArgumentParser Pattern

Clean way to code an `ArgumentParser` instance.

**Usage**  
Just see code.

[code](/junkdrawer/arg_parser.py)

### 2. File Log Creator

Simple wrapper for creating Python logger instances with file handlers.

**Purpose**
- I frequently just need to initialize a logger with a handler to a file. I didnt like having to rewrite all the handler init and config every time.
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

### 3. Compare Storage Perfomance of Python Data Structures

Evaluate the memory performance of the following data structures for a data object:
- dict
- list
- data classes
- slots classes

[code](junkdrawer/dict_vs_list_vs_dataclass_vs_slots.py)

**Usage**

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
```yml
# data_model.yml
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

```sh
>>python dict_vs_list_vs_dataclass_vs_slots.py -d data_model.yml -n 100000
n is 100000
Size of data classes: 824456 bytes
Size of slots classes: 216825080 bytes
Size of lists: 219225080 bytes
Size of dicts: 242425584 bytes
```

### 4. JSON-like data filter

A filter function that can work on any JSON-like data structure (i.e. lists, dicts, and values). The filter function takes a list of the JSON-like data instances and then applies filters (specified by simple filter format) to them. Filters can be supplied to filter out matching instances or filter in matching instances. The filters can be for string matches, substring check (via python "in"), re.search pattern or re.match pattern. Filters may also be flagged to be applied separately as a set (i.e. compound filter).

**Purpose**

[code](/junkdrawer/json_data_struct_filter.py)

**Usage**
```
(TODO)
```

### 5. Nested dictionary and list access

_(not coded by maintainer, see module docstrings for reference)_

Utility functions for nested dictionary and list access.

[code](junkdrawer/nested_dict_access_by_key_list.py)

**Usage**  
```python
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

# Use Python "in" operator on nested dict/list
#
# Note how lists are navigated here. We navigate to dict with
# key '3', then jump to index 1, then back to key "4
>>> d
{'1': {'2': {'3': ['seldon', {'4': 'mallow'}]}}}
>>> in_nested_path(d, ["1", "2", "3", 1, "4"])
True
```

### 6. Class-Function IO Monitor

Wrap classes and functions to record all input and output.

[code](junkdrawer/func_io_monitor.py)

**Usage**  
```python
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
```

### 7. Flask App Skeleton

A useful Flask skeleton to jumpstart a Flask web/REST API framework.

See dedicated [Flask App README](junkdrawer/flask_skeleton/) for documentation.
