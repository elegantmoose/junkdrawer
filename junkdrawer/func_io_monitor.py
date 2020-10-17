"""
Function and Class I/O Monitor

A utility for wrapping functions and classes in order to record all input and output to functions/methods.

Use Cases:
- Creating input/output data for unit testing.

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


from enum import Enum
import inspect
import json
import logging
import os
import time


class RecordTypes(Enum):
    log = 0
    json = 1

    
RECORD_TYPES = RecordTypes


def func_io_monitor(func, record_type=RECORD_TYPES.log, record_fp=None, recorder=None, input_log_formatter=None, output_log_formatter=None):
    """Creates a monitored I/O version of the function.
    
    Supplied function is not altered.
    
    Args:
        func(func): function or method to wrap
        logger (logger): python logging instance
        record_fp ():
        record_type ():
        input_log_formatter (func): a callable to use to format function input for logging.
        output_log_formatter (func): a callable to use to format function output for logging.

    Returns: (func) monitored function
    """
    if not recorder:
        recorder = _get_recorder(record_type, record_fp)
    
    def io_monitor(*args, **kwargs):
        if "__self__" in dir(func):
            func_class = str(func.__self__).split(" ")[0].strip("<")
            func_key = ".".join([func_class, func.__name__])
        else:
            func_class = "<none>"
            func_key = ".".join([func.__module__,func_class, func.__name__])
        if input_log_formatter:
            input_ = input_log_formatter(*args, **kwargs)
        else:
            # default - json structured str
            input_ = {"args": args, "kwargs": kwargs}
        output = func(*args, **kwargs)
        if output_log_formatter:
            r_output = output_log_formatter(output)
        else:
            # default - convert to str
            r_output = str(output)
        recorder.record(func_key, input_, r_output)
        return output
        
    return io_monitor
    
    
def class_io_monitor(class_instance, record_type=RECORD_TYPES.log, record_fp=None, recorder=None, func_input_log_formatters=None, func_ouput_log_formatters=None):
    """Converts class instance to instance where every component method is I/O monitored.

    The returned class instance has all its methods replaced with monitored versions.

    Args:
        class_instance (obj): class instance to convert

    Returns: (obj) class instance
    """
    # create io monitor methods for every method in class instance
    if not recorder:
        recorder = _get_recorder(record_type, record_fp)
    wrapped_methods = {}
    for attr in dir(class_instance):
        if inspect.ismethod(getattr(class_instance, attr)):
            wrapped_methods[attr] = func_io_monitor(getattr(class_instance, attr), recorder=recorder)
    # replace class instance methods with wrapped monitor versions
    for name, monitor_method in wrapped_methods.items():
        setattr(class_instance, name, monitor_method)  
    return class_instance
      
      
 # -- Internal --


def _get_recorder(record_type, record_fp):
    """ """
    if record_type == RECORD_TYPES.log:
        return _recorder_log(record_fp)
    elif record_type == RECORD_TYPES.json:
        return _recorder_json(record_fp)
    else:
        raise ValueError("Recorder type not found")

        
class _recorder_log:
    """ """
    def __init__(self, fp=None):
        enabled = True if fp else False
        fp = fp if fp else "fangless"
        self.log = _get_logger(fp, enabled=enabled, log_level="INFO")
    def record(self, function_key, input_, output):
        """ """
        self.log.info(f"{function_key} - IN: {input_} - OUT: {output}")
        
 
class _recorder_json:
    """ """
    def __init__(self, fp):
        self.fp = os.path.abspath(fp)
    def record(self, function_key, input_, output):
        """ """
        if os.path.isfile(self.fp):
            e_json = json.load(open(self.fp, 'r'))
        else:
            e_json = {}
        if function_key not in e_json.keys():
            e_json[function_key] = []
        e_json[function_key].append(
            {
                "time": time.time(),
                "in": input_,
                "out": output
            }
        )
        json.dump(e_json, open(self.fp, 'w'))
    

def _get_logger(fp, enabled=True, log_level="INFO"):
    """Create a logger that outputs to supplied filepath
    Args:
        enabled (bool): Whether logging is enabled. This function is called
            in scripts that call it with suppied arguments, and allows the
            scripts this utility blindly.
        fp (str): filename of the log
        log_level (str): Python logging level to set
        
    Returns:
        (logging.logger) logging handle
    """
    # no matter what a fangless logger is created (for cleaner code)
    logger = logging.getLogger(fp.split("/")[-1].split(".")[0])
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s \n',
                                  datefmt="%Y-%m-%d %H:%M:%S")
    
    if enabled:
        # set filehandler
        fh = logging.FileHandler(fp, mode='w')
        fh.setFormatter(formatter)
        fh.setLevel(getattr(logging, log_level.upper()))
        logger.addHandler(fh)

    return logger
     

