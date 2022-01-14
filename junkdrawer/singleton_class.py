```
Ref: https://github.com/mitre/human/blob/master/pyhuman/app/utility/base_driver.py
    
@author: https://github.com/djlawren
    
Allows for the creation of a singleton class within a Python execution environment.
```

from abc import abstractmethod


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseClass(metaclass=Singleton):

    __slots__ = ['name']

    @abstractmethod
    def __init__(self, name: str):
        self.name = 
