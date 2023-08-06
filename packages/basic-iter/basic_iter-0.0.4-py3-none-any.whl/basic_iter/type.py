"""Type variables and aliases used in basic_iter."""

from typing import (TypeVar, Callable)

S = TypeVar("S")
"""A type variable identified by 'S'."""
T = TypeVar("T")
"""A type variable identified by 'T'."""
U = TypeVar("U")
"""A type variable identified by 'U'."""

T1 = TypeVar("T1")
"""A type variable identified by 'T1'."""
T2 = TypeVar("T2")
"""A type variable identified by 'T2'."""
T3 = TypeVar("T3")
"""A type variable identified by 'T3'."""
T4 = TypeVar("T4")
"""A type variable identified by 'T4'."""
T5 = TypeVar("T5")
"""A type variable identified by 'T5'."""
T6 = TypeVar("T6")
"""A type variable identified by 'T6'."""
T7 = TypeVar("T7")
"""A type variable identified by 'T7'."""

Predicate = Callable[[T], bool]
"""A predicate on a type `T`."""
