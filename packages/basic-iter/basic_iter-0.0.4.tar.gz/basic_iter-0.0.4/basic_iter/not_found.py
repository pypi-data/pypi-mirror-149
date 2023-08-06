"""
This module provides `NotFound` represents that something is not found.
"""
from typing import Any


class NotFound:
    """
    Represents that something was not found.

    An instance of this class indicates that something was not found.
    These values are constructed by functions that look for the values of something such like `find <basic_iter.prim_list.find>`.
    """

    __cond: Any

    def __init__(self, cond: Any):
        self.__cond = cond

    def __str__(self) -> str:
        if callable(self.__cond):
            return f"Not found items satisfy the condition {self.__cond}"
        else:
            return f"Not found items equal to the value {self.__cond}"

    def __repr__(self) -> str:
        return f"NotFound({repr(self.__cond)})"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
