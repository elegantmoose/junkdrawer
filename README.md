# junkdrawer
Useful Python utilities and patterns for a career python developer.

## Class/Function input/output monitor

```sh
Usage:
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
