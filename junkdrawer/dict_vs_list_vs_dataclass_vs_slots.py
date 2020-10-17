"""
Compare data structure storage performance of:
  - dict
  - list
  - dataclasses
  - slots
"""


from pympler import asizeof
from dataclasses import dataclass
import uuid
import random


# TODO: Allow user to supply n parameter
# TODO: Allow user to supply data model (yaml file or something) and then build up objects dynamically, thus dont have to change static coding of objects.


class MK(object):
    __slots__ = ["uuid_1", "uuid_2", "int_1", "int_2", "float_1", "float_2"]
    def __init__(self, uuid_1, uuid_2, int_1, int_2, float_1, float_2):
        self.uuid_1 = uuid_1
        self.uuid_2 = uuid_2
        self.int_1 = int_1
        self.int_2 = int_2
        self.float_1 = float_1
        self.float_2 = float_2
        
   
@dataclass
class MKDC:
    uuid_1: str
    uuid_2: str
    int_1: int
    int_2: int
    float_1: float
    float_2: float


def main():
    n= 100000
    dicts = []
    lists = []
    slots = []
    data_classes = []
    for i in range(n):
        uuid_1 = uuid.uuid4()
        uuid_2 = uuid.uuid4()
        int_1 = random.randint(1, 10**8)
        int_2 = random.randint(1, 10**8)
        float_1 = random.random()
        float_2 = random.random()
        dicts.append({"uuid_1": uuid_1,
                      "uuid_2": uuid_2,
                      "int_1": int_1, 
                      "int_2": int_2,
                      "float_1": float_1,
                      "float_2": float_2})
        lists.append([uuid_1, uuid_2, int_1, int_2, float_1, float_2])
        slots.append(CS(uuid_1, uuid_2, int_1, int_2, float_1, float_2))
        data_classes.append(MKDC(uuid_1, uuid_2, int_1, int_2, float_1, float_2))

    print(f"n is {n}")
    print(f"Size of dicts: {asizeof.asizeof(dicts)}")
    print(f"Size of lists: {asizeof.asizeof(lists)}")
    print(f"Size of slots: {asizeof.asizeof(slots)}")
    print(f"Size of slots: {asizeof.asizeof(data_classes)}")



if __name__ == "__main__":
    main()
