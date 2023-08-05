

from abc import ABC
from typing import Callable


class Operation(ABC):
    """Field operation
    """
    __py_magic__: str

    def __init__(self, value):
        self.value = value

    def _get_formatter(self, result:'BaseResult') -> Callable:
        return getattr(result, self.__formatter__)

    def evaluate(self, value):
        return getattr(self, self.__py_magic__)(value)

class GreaterThan(Operation):
    __py_magic__ = "__gt__"
    __formatter__ = "format_greater_than"
    def __gt__(self, value):
        return value > self.value

class LessThan(Operation):
    __py_magic__ = "__lt__"
    __formatter__ = "format_less_than"
    def __lt__(self, value):
        return value < self.value

class GreaterEqual(Operation):
    __py_magic__ = "__ge__"
    __formatter__ = "format_greater_equal"
    def __lt__(self, value):
        return value >= self.value

class LessEqual(Operation):
    __py_magic__ = "__le__"
    __formatter__ = "format_less_equal"
    def __lt__(self, value):
        return value <= self.value


def greater_than(value):
    return GreaterThan(value)
    
def less_than(value):
    return LessThan(value)

def greater_equal(value):
    return GreaterEqual(value)
    
def less_equal(value):
    return LessEqual(value)