"""
Some basic operators on the primitive list.

Almost functions behave on the primitive list in the same way as the function of the same name
provided in `Data.List <https://hackage.haskell.org/package/base-4.10.1.0/docs/Data-List.html>`_ from Haskell that is a purely functional language.
Therefore, all functions are defined in the functional style and do not change their arguments.

However, some functions are not exactly the same as in Haskell.

- `and_list` function is defined as `and` in Haskell, but is renamed because it is a keyword in Python.
  `or_list` is renamed from `or` for the same reason as `and_list`.

- Find-family functions (e.g. `find`, `lookup`, etc...) returns a value of `Found[T] <basic_iter.found.Found>` instead of `Optional[T]`.
  This is because `Optional` cannot distinguish whether nothing was found or `None` was found.
  That is, if it returns `Optional`, :code:`find(lambda x: x is None, xs)` always returns `None`.
"""

import copy

from typing import (
    Generator,
    List,
    Callable,
    Tuple,
    Optional,
)
from .found import Found
from .type import *


def last(xs: List[T]) -> T:
    """
    Extract the last element of a list, which must be non-empty.

    Raises:
      AssertionError: `xs` is not empty.
    """
    assert not (null(xs)), "must not to be empty"
    return xs[-1]


def head(xs: List[T]) -> T:
    """
    Extract the head of the list `xs`, which must to be non-empty.

    Raises:
      AssertionError: `xs` is not empty.
    """
    assert not null(xs), "must not to be empty"
    return xs[0]


def tail(xs: List[T]) -> List[T]:
    """
    Extract elements after the head of the list `xs`, which must be non-empty.

    Raises:
      AssertionError: `xs` is not empty.
    """
    assert not (null(xs)), "must not to be empty"
    return xs[1:]


def init(xs: List[T]) -> List[T]:
    """
    Extract elements except the last element of the list `xs`, which must be non-empty.

    Raises:
      AssertionError: `xs` is not empty.
    """
    assert not (null(xs)), "must not to be empty"
    return xs[0:len(xs) - 1]


def uncons(xs: List[T]) -> Optional[Tuple[T, List[T]]]:
    """
    Decompose a list into its head and tail.
    If the list is empty, returns `None`.
    If non-empty, returns :code:`(x, xs)`, where `x` is the head of the list and `xs` its tail.

    Returns:
      If the list is empty, returns `None`.
      If the list is non-empty, returns :code:`(head(x), tail(xs))`.

    Examples:
      >>> uncons([])
      >>> uncons([1,2,3])
      (1, [2, 3])
    """
    if null(xs):
        return None
    else:
        return (head(xs), tail(xs))


def null(xs: List[T]) -> bool:
    """
    Checks if the list `xs` is empty.

    Returns:
      the list is empty or not.
    """
    return not xs


def append(xs: List[T], ys: List[T]) -> List[T]:
    """
    A list of appended `xs` and `ys`.

    Returns:
      A list where `xs` is followed by `ys`.

    Examples:
      >>> xs = [1,2,3]; ys = [4,5,6]; append (xs, ys)
      [1, 2, 3, 4, 5, 6]
      >>> append ([1,2,3], [])
      [1, 2, 3]
      >>> append ([], [1,2,3])
      [1, 2, 3]
      >>> append ('hello', ' world')
      'hello world'
    """
    return xs + ys


# pylint: disable-next=redefined-builtin
def map(f: Callable[[T], U], xs: List[T]) -> List[U]:
    """
    Mapping all elements in the list `xs` to the result list with a mapping function `f`.

    Examples:
      >>> map (lambda x: x * 2, [1,2,3])
      [2, 4, 6]
      >>> map (str, [1,2,3])
      ['1', '2', '3']
    """
    return [f(x) for x in xs]


def reverse(xs: List[T]) -> List[T]:
    """
    Reverse the list `xs`.

    Returns:
      A list of `xs` elements in reverse order.

    Examples:
      >>> reverse([1,2,3])
      [3, 2, 1]
      >>> "".join(reverse(list('foobarbaz')))
      'zabraboof'
    """
    return xs[-1:-len(xs) - 1:-1]


def intersperse(e: T, xs: List[T]) -> List[T]:
    """
    Intersperses an element `e` between the elements of the list `xs`.

    Examples:
      >>> intersperse (',', [])
      []
      >>> intersperse (',', list('abcde'))
      ['a', ',', 'b', ',', 'c', ',', 'd', ',', 'e']
      >>> intersperse (',', 'a')
      ['a']
    """
    if null(xs):
        return []

    res: List[T] = [xs[0]]
    for x in xs[1:]:
        res.extend([e, x])
    return res


def intercalate(xs: List[T], xxs: List[List[T]]) -> List[T]:
    """
    Intercalate `xs` between member lists in `xxs`.

    Examples:
      >>> "".join(intercalate(list(" and "), map(list, ["apple", "orange", "grape"])))
      'apple and orange and grape'
    """
    if null(xxs):
        return []
    res: List[T] = copy.copy(xxs[0])
    for ys in xxs[1:]:
        res += xs
        res += ys
    return res


def transpose(xxs: List[List[T]]) -> List[List[T]]:
    """
    Transpose rows and columns of `xxs`.
    If some of the rows are shorter than the following rows, their elements are skipped.

    Example:
        >>> transpose ([[1,2,3],[4,5,6]])
        [[1, 4], [2, 5], [3, 6]]
        >>> transpose ([[10,11],[20],[],[30,31,32]])
        [[10, 20, 30], [11, 31], [32]]
    """
    if null(xxs):
        return []

    col = max(map(len, xxs))
    rss: List[List[T]] = []
    for i in range(col):
        # construct i-th line vector from i-th column elements
        rs: List[T] = []
        # pylint: disable-next=cell-var-from-loop
        for xs in filter(lambda xs: len(xs) > i, xxs):
            rs.append(xs[i])
        rss.append(rs)
    return rss


def subsequences(xs: List[T]) -> List[List[T]]:
    """
    Enumerates all subsequences of the given list `xs`.

    Examples:
      >>> subsequences([])
      [[]]
      >>> subsequences(list("abc"))
      [[], ['a'], ['a', 'b'], ['a', 'b', 'c'], ['a', 'c'], ['b'], ['b', 'c'], ['c']]
    """
    res: List[List[T]] = [[]]
    for i, x in enumerate(xs):
        # pylint: disable-next=cell-var-from-loop
        res += map(lambda ys: [x] + ys, subsequences(xs[i + 1:]))
    return res


def permutations(xs: List[T]) -> List[List[T]]:
    """
    Create a list of all permutations combinations of the given list `xs`.

    Returns:
      The list of permutations of the list `xs`.

    Examples:
      >>> permutations([1,2,3])
      [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """
    if null(xs):
        return [[]]

    res: List[List[T]] = []
    ys: List[T] = copy.copy(xs)
    for i in range(len(xs)):
        y = ys.pop(i)
        # pylint: disable-next=cell-var-from-loop
        res += map(lambda xs: [y] + xs, permutations(ys))
        ys.insert(i, y)
    return res


def foldl(f: Callable[[U, T], U], e: U, xs: List[T]) -> U:
    """
    Folding left-to-right the list `xs` with the function `f` start from `e`.
    For the list `xs` is ``[ x0, x1, x2, ... , x(n-1), xn ]``,
    a calculation equivalent to the following expression is performed::

      f (xn, f (x(n-1), ... f (x2, f (x1, f (x0, e)))))

    Returns:
      A left-to-right folding of the list `xs` with the function `f`.

    Examples:
      >>> foldl (lambda acc, x: x + acc, 0, list(range(1, 11)))
      55
      >>> foldl (lambda acc, x: [x] + acc, [0], list(range(1, 6)))
      [5, 4, 3, 2, 1, 0]
      >>> foldl (lambda acc, x: [x] + [acc], [0], list(range(1, 6)))
      [5, [4, [3, [2, [1, [0]]]]]]
    """
    acc = e
    for x in xs:
        acc = f(acc, x)
    return acc


def foldl1(f: Callable[[T, T], T], xs: List[T]) -> T:
    """
    A variant of `foldl` that has no base case.
    Thus, this may only be applied to non-empty lists.

    Returns:
      A left-to-right folding of the list `xs` with the function `f`.

    Raises:
      AssertionError: `xs` is empty.

    Examples:
      >>> foldl1 (lambda acc, x: x + acc, list(range(1, 11)))
      55
      >>> foldl1 (lambda acc, x: [x] + ([acc] if 1 == acc else acc), list(range(1, 6)))
      [5, 4, 3, 2, 1]

    Example:
      This fragment cause type errors, it is showed to help you understand behaviour.

      >>> foldl1 (lambda acc, x: [x] + [acc], list(range(1, 6)))
      [5, [4, [3, [2, 1]]]]
    """
    assert xs, "required to be a non-empty list"
    return foldl(f, xs[0], xs[1:])


def foldr(f: Callable[[T, U], U], e: U, xs: List[T]) -> U:
    """
    Folding right-to-left the list `xs` with the function `f` start from `e`.
    For the list `xs` is ``[ x0, x1, x2, ... , x(n-1), xn ]``,
    a calculation equivalent to the following expression is performed::

      f (x0, f (x1, ... f (x(n-2), f (x(n-1), f (xn, e)))))

    Returns:
      A right-to-left folding of the list `xs` with the function `f`.

    Example:
      Sum all values in a list.

      >>> foldr (lambda x, acc: x + acc, 100, list(range(10)))
      145

    Examples:
      >>> foldr (lambda x, acc: [x] + acc, [5], list(range(5)))
      [0, 1, 2, 3, 4, 5]
      >>> foldr (lambda x, acc: [x] + [acc], [5], list(range(5)))
      [0, [1, [2, [3, [4, [5]]]]]]
    """
    acc = e
    for x in reverse(xs):
        acc = f(x, acc)
    return acc


def foldr1(f: Callable[[T, T], T], xs: List[T]) -> T:
    """
    Folding right-to-left the non-empty list `xs` with the function `f`.
    For the list `xs` is ``[ x0, x1, x2, ... , x(n-1), xn ]``,
    a calculation equivalent to the following expression is performed::

      f (x0, f (x1, ... f (x(n-2), f (x(n-1), f (xn, e)))))

    Returns:
      A right-to-left folding of the list `xs` with the function `f`.

    Raises:
      AssertionError: `xs` is empty.

    Example:
      Sum all values in a list.

      >>> foldr1 (lambda x, acc: x + acc, list(range(10)))
      45

    Example:
      >>> # 0 - (1 - (2 - (3 - 4)))
      >>> foldr1 (lambda x, acc: x - acc, list(range(5)))
      2
    """
    assert xs, "required to be a non-empty list"
    return foldr(f, last(xs), init(xs))


def concat(xxs: List[List[T]]) -> List[T]:
    """
    Construct a list from the list of list `xxs`.
    This is a directly concatenated list of elements of the list `xxs`.

    Returns:
      A concatenated list of elements of the list `xxs`.

    Examples:
      >>> concat([[1,2,3], [4,5,6], [7,8,9]])
      [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    res: List[T] = []
    for xs in xxs:
        res += xs
    return res


def concat_map(f: Callable[[T], List[U]], xs: List[T]) -> List[U]:
    """
    Map the function `f` over all elements of the list `xs`, and concatenate the resulting lists.

    Returns:
      A concatinated list of mapped elements of the list `xs`.

    Examples:
      >>> concat_map(lambda x: [x, x+1], [1,2,3,4,5])
      [1, 2, 2, 3, 3, 4, 4, 5, 5, 6]
    """
    res: List[U] = []
    for x in xs:
        res += f(x)
    return res


def and_list(xs: List[bool]) -> bool:
    """
    This is provided as `and` in `Data.List <https://hackage.haskell.org/package/base-4.10.1.0/docs/Data-List.html>`_.
    Since this is the keyword in Python, it is renamed.

    Returns:
      Whether the all elements of the list `xs` is `True`.
    """
    for x in xs:
        if not x:
            return False
    return True


def or_list(xs: List[bool]) -> bool:
    """
    This is provided as `or` in `Data.List <https://hackage.haskell.org/package/base-4.10.1.0/docs/Data-List.html>`_.
    Since this is the keyword in Python, it is renamed.

    Returns:
      Whether any elements of the list `xs` is `True`.
    """
    for x in xs:
        if x:
            return True
    return False


# pylint: disable-next=redefined-builtin
def any(p: Predicate[T], xs: List[T]) -> bool:
    """
    Check any elements of the list `xs` satisfy the predicate `p`.

    Examples:
      >>> any(lambda x: x % 2 == 0, [1,3,5,7,9])
      False
      >>> import re
      >>> any(lambda x: re.search(r'a*b{2}c', x), ['bc', 'ab', 'aaabbc'])
      True
    """
    for x in xs:
        if p(x):
            return True
    return False


# pylint: disable-next=redefined-builtin
def all(p: Predicate[T], xs: List[T]) -> bool:
    """
    Check all elements of the list `xs` satisfy the predicate `p`.

    Examples:
      >>> all(lambda x: x % 2 == 0, [0,2,4,6,7])
      False
      >>> import re
      >>> all(lambda x: re.search(r'a*b', x), ['abc', 'b', 'aaab'])
      True
    """
    for x in xs:
        if not p(x):
            return False
    return True


def scanl(f: Callable[[U, T], U], e: U, xs: List[T]) -> List[U]:
    """
    Folding left-to-right the list and returns a list of the intermediate values.
    For the input list `xs` and the result list are
    ``[ x0, x1, x2, ... , x(n-1), xn ]`` and ``[ r0, r1, ..., r(n-1), rn, r(n+1) ]``::

      r0     is calculated from foldl f e      [  ]
      r1     is calculated from foldl f r0     [x0]
      ...
      rn     is calculated from foldl f r(n-1) [x(n-1)]
      r(n+1) is calculated from foldl f rn     [xn].

    Returns:
      A list of intermediate foldl values with the function `f`.

    Examples:
      >>> scanl (lambda acc, x: x + acc, 0, list(range(1, 6)))
      [0, 1, 3, 6, 10, 15]
      >>> scanl (lambda acc, x: [x] + acc, [], list(range(1, 6)))
      [[], [1], [2, 1], [3, 2, 1], [4, 3, 2, 1], [5, 4, 3, 2, 1]]
    """
    acc = e
    res = [acc]
    for x in xs:
        acc = f(acc, x)
        res.append(acc)
    return res


def scanl1(f: Callable[[T, T], T], xs: List[T]) -> List[T]:
    """
    scanl1 is a variant of scanl that has no starting value argument

    Raises:
      AssertionError: `xs` is empty.
    """
    assert xs, "required to be a non-empty list"
    return scanl(f, xs[0], xs[1:])


def scanr(f: Callable[[T, U], U], e: U, xs: List[T]) -> List[U]:
    """
    Folding right-to-left the list and returns a list of the intermediate values.
    For the input list `xs` and the result list are
    ``[ x0, x1, x2, ... , x(n-1), xn ]`` and ``[ r0, r1, ..., r(n-1), rn, r(n+1) ]``::

      r0     is calculated from foldr f r1     [x0]
      r1     is calculated from foldr f r2     [x1]
      ...
      rn     is calculated from foldr f r(n+1) [xn]
      r(n+1) is calculated from foldr f e      [  ]

    Returns:
      A list of intermediate foldr values with the function `f`.

    Examples:
      >>> scanr (lambda x, acc: x + acc, 5, list(range(1, 5)))
      [15, 14, 12, 9, 5]
      >>> scanr (lambda x, acc: [x] + acc, [], list(range(1, 6)))
      [[1, 2, 3, 4, 5], [2, 3, 4, 5], [3, 4, 5], [4, 5], [5], []]
      >>> scanr (max, 18, [3,6,12,4,55,11])
      [55, 55, 55, 55, 55, 18, 18]
    """
    acc = e
    res = [acc]
    for x in reverse(xs):
        acc = f(x, acc)
        res.append(acc)
    res.reverse()
    return res


def map_accuml(f: Callable[[T, U], Tuple[T, S]], e: T, xs: List[U]) -> Tuple[T, List[S]]:
    """
    map_accuml transforms the list `xs` with `f` and
    simultaneously accumulates its elements from left-to-right into a value of `T`.

    Returns:
      A tuple of the accumulated value and the transformed list.

    Examples:
      >>> map_accuml(lambda acc, x: (x+acc, str(x)), 0, range(1,5))
      (10, ['1', '2', '3', '4'])
    """
    acc: T = e
    ys: List[S] = []
    for x in xs:
        acc, c = f(acc, x)
        ys.append(c)
    return (acc, ys)


def map_accumr(f: Callable[[T, U], Tuple[T, S]], e: T, xs: List[U]) -> Tuple[T, List[S]]:
    """
    map_accumr transforms the list `xs` with `f` and
    simultaneously accumulates its elements from right-to-left into a value of `T`.

    Returns:
      A tuple of the accumulated value and the transformed list.

    Examples:
      >>> map_accumr(lambda acc, x: (x+acc, str(x)), 0, range(1,5))
      (10, ['4', '3', '2', '1'])
    """
    acc: T = e
    ys: List[S] = []
    for x in reverse(xs):
        acc, c = f(acc, x)
        ys.append(c)
    return (acc, ys)


def replicate(n: int, x: T) -> List[T]:
    """
    Replicate the value `x` `n` times.
    When the value of `n` is less than 0, an empty list is returned.

    Returns:
      The list of length `n` with `x` the value of every element.

    Examples:
      >>> replicate (0, 1)
      []
      >>> replicate (3, "foo")
      ['foo', 'foo', 'foo']
      >>> replicate (-5, 1)
      []
    """
    if n < 0:
        return []

    xs: List[T] = []
    for _ in range(n):
        xs.append(x)

    return xs


# pylint: disable-next=redefined-outer-name
def unfoldr(f: Callable[[T], Optional[Tuple[U, T]]], init: T) -> List[U]:
    """
    Builds a list from the seed value `init` with `f`.
    The function `f` takes a seed value and returns `None`
    if it is done producing the list or tuple :code:`(u, t)`, in which case,
    the `u` value is next element of a list and
    the `t` is the seed value for the next element generating.

    Execution steps is as follows::

      unfoldr (\\x: None if x > 5 else (x*2,x+1), 0)
      ==> [0] + unfoldr (\\x: None if x > 5 else (x*2,x+1), 1) by not 0 > 5
      ==> [0,2] + unfoldr (\\x: None if x > 5 else (x*2,x+1), 2) by not 1 > 5
      ==> [0,2,4] + unfoldr (\\x: None if x > 5 else (x*2,x+1), 3) by not 2 > 5
      ==> [0,2,4,6] + unfoldr (\\x: None if x > 5 else (x*2,x+1), 4) by not 3 > 5
      ==> [0,2,4,6,8] + unfoldr (\\x: None if x > 5 else (x*2,x+1), 5) by not 4 > 5
      ==> [0,2,4,6,8,10] + unfoldr (\\x: None if x > 5 else (x*2,x+1), 6) by not 5 > 5
      ==> [0,2,4,6,8,10] + [] by 6 > 5


    Returns:
      The generated list from the `init` with `f`.

    Examples:
      >>> unfoldr (lambda x: None if x > 5 else (x*2, x+1), 0)
      [0, 2, 4, 6, 8, 10]
      >>> unfoldr (lambda x: (x,x+1) if x < 5 else None, 0)
      [0, 1, 2, 3, 4]
    """
    res: List[U] = []
    elm = init
    while True:
        r = f(elm)
        if r:
            (x, e) = r
            res.append(x)
            elm = e
        else:
            break
    return res


def take(n: int, xs: List[T]) -> List[T]:
    """
    Returns:
      The prefix of `xs` of length `n`.

    Examples:
      >>> take (3, [1,2,3,4,5])
      [1, 2, 3]
      >>> take (6, [1,2,3,4,5])
      [1, 2, 3, 4, 5]
      >>> take (-1, [1,2,3,4,5])
      []
    """
    if n < 0:
        return []
    return xs[0:n]


def drop(n: int, xs: List[T]) -> List[T]:
    """
    Returns:
      The suffix of `xs` after the first `n` elements.

    Examples:
      >>> drop (3, [1,2,3,4,5])
      [4, 5]
      >>> drop (6, [1,2,3,4,5])
      []
      >>> drop (-1, [1,2,3,4,5])
      [1, 2, 3, 4, 5]
    """
    if n < 0:
        return xs
    return xs[n:]


def split_at(n: int, xs: List[T]) -> Tuple[List[T], List[T]]:
    """
    Split the list `xs` into a tuple where first element is `xs` prefix of length `n`
    and second element is suffix of `xs` after the first `n` elements.

    Examples:
      >>> split_at (3, [1,2,3,4,5])
      ([1, 2, 3], [4, 5])
      >>> split_at (6, [1,2,3,4,5])
      ([1, 2, 3, 4, 5], [])
      >>> split_at (-1, [1,2,3,4,5])
      ([], [1, 2, 3, 4, 5])
    """
    return (take(n, xs), drop(n, xs))


def take_while(p: Predicate[T], xs: List[T]) -> List[T]:
    """
    The longest prefix of the list `xs` of elements that satisfy `p`.

    Examples:
      >>> take_while (lambda n: n >= 10, [13, 12, 11, 10, 9, 8])
      [13, 12, 11, 10]
      >>> take_while (lambda n: n%2 == 0, [12, 10, 9, 8, 7])
      [12, 10]
      >>> take_while (lambda n: n < 0, [0, 3, -3, 5, -5])
      []
    """
    for i, x in enumerate(xs):
        if not p(x):
            return xs[0:i]
    return xs


def drop_while(p: Predicate[T], xs: List[T]) -> List[T]:
    """
    The suffix of the list `xs` remaining after `take_while(p, xs) <take_while>`.

    Examples:
      >>> drop_while (lambda n: n >= 10, [13, 12, 11, 10, 9, 8])
      [9, 8]
      >>> drop_while (lambda n: n%2 == 0, [12, 10, 9, 8, 7])
      [9, 8, 7]
      >>> drop_while (lambda n: n < 0, [0, 3, -3, 5, -5])
      [0, 3, -3, 5, -5]
    """
    for i, x in enumerate(xs):
        if not p(x):
            return xs[i:]
    return []


def drop_while_end(p: Predicate[T], xs: List[T]) -> List[T]:
    """
    The suffix of the list `xs` remaining after `take_while(p, xs) <take_while>`.

    Examples:
      >>> drop_while_end (lambda n: n >= 10, [13, 12, 11, 10, 9, 8])
      [13, 12, 11, 10, 9, 8]
      >>> drop_while_end (lambda n: n%2 != 0, [12, 10, 9, 8, 7])
      [12, 10, 9, 8]
      >>> drop_while_end (lambda n: n < 0, [0, 3, -3, 5, -5])
      [0, 3, -3, 5]
    """
    n: int = len(xs)
    for i, x in enumerate(reverse(xs)):
        if not p(x):
            return xs[0:n - i]
    return []


def span(p: Predicate[T], xs: List[T]) -> Tuple[List[T], List[T]]:
    """
    A tuple where first element is the longest prefix of `xs` of elements
    that satisfy `p` and second element is the remainder of the list.

    Examples:
      >>> span (lambda n: n >= 10, [13, 12, 11, 10, 9, 8])
      ([13, 12, 11, 10], [9, 8])
      >>> span (lambda n: n%2 != 0, [12, 10, 9, 8, 7])
      ([], [12, 10, 9, 8, 7])
      >>> span (lambda n: abs(n) < 10, [0, 3, -3, 5, -5])
      ([0, 3, -3, 5, -5], [])
    """
    return (take_while(p, xs), drop_while(p, xs))


def break_to(p: Predicate[T], xs: List[T]) -> Tuple[List[T], List[T]]:
    """
    A tuple where first element is the longest prefix of `xs` of elements
    that do not satisfy `p` and second element is the remainder of the list.

    Examples:
      >>> break_to (lambda x: x > 3, [1, 2, 3, 4, 1, 2, 3, 4])
      ([1, 2, 3], [4, 1, 2, 3, 4])
      >>> break_to (lambda x: x < 9, [1, 2, 3])
      ([], [1, 2, 3])
      >>> break_to (lambda x: x > 9, [1, 2, 3])
      ([1, 2, 3], [])
    """
    return span(lambda x: not p(x), xs)


def group(xs: List[T]) -> List[List[T]]:
    """
    Equivalent to calling `group_by` on `==`.

    Examples:
      >>> group ([1,1,1,2,2,3,3,3,3])
      [[1, 1, 1], [2, 2], [3, 3, 3, 3]]
      >>> group ([])
      []
    """
    return group_by(lambda x, y: x == y, xs)


def strip_prefix(xs: List[T], ys: List[T]) -> Optional[List[T]]:
    """
    Strip of the prefix `xs` from `ys`.

    Returns:
      None is returned when the `xs` is not the prefix of `ys`.
      If the list `ys` starts from `xs`, returns the remaining of the prefix `xs`.

    Examples:
      >>> strip_prefix (["f", "o", "o"], ["f", "o", "o", "b", "a", "r"])
      ['b', 'a', 'r']
      >>> strip_prefix (["f", "o", "o"], ["f", "o", "o"])
      []
      >>> strip_prefix (["f", "o", "o"], ["b", "a", "r", "f", "o", "o"])
      >>> strip_prefix (["f", "o", "o"], ["b", "a", "r", "f", "o", "o", "b", "a", "z"])
      >>> strip_prefix (["f", "o", "o", "b", "a", "r"], ["f", "o", "o"])
    """
    if xs == ys[0:len(xs)]:
        return ys[len(xs):]
    else:
        return None


def inits(xs: List[T]) -> List[List[T]]:
    """
    Returns:
      A list of the prefix of the list `xs`, shortest first.

    Examples:
      >>> inits(['a', 'b', 'c'])
      [[], ['a'], ['a', 'b'], ['a', 'b', 'c']]
    """
    res: List[List[T]] = []
    for i in range(len(xs) + 1):
        res.append(xs[0:i])
    return res


def tails(xs: List[T]) -> List[List[T]]:
    """
    Returns:
      A list of all final segments of the list `xs`, longest first.

    Examples:
      >>> tails(['a', 'b', 'c'])
      [['a', 'b', 'c'], ['b', 'c'], ['c'], []]
    """
    res: List[List[T]] = []
    for i in range(len(xs) + 1):
        res.append(xs[i:])
    return res


def is_prefix_of(xs: List[T], ys: List[T]) -> bool:
    """
    Check the list `xs` is equals to the prefix of the list `ys`.

    Examples:
      >>> is_prefix_of ([1,2,3], [1,2,3,4,5])
      True
      >>> is_prefix_of ([3,4,5], [1,2,3,4,5])
      False
      >>> is_prefix_of ([3,42,5], [3,42])
      False
    """
    return len(ys) >= len(xs) and ys[0:len(xs)] == xs


def is_suffix_of(xs: List[T], ys: List[T]) -> bool:
    """
    Check the list `xs` is equals to the suffix of the list `ys`.

    Examples:
      >>> is_suffix_of ([3,4,5], [1,2,3,4,5])
      True
      >>> is_suffix_of ([2,3,4], [1,2,3,4,5])
      False
      >>> is_suffix_of ([], [3,42])
      True
    """
    return len(ys) >= len(xs) and ys[len(ys) - len(xs):len(ys)] == xs


def is_infix_of(xs: List[T], ys: List[T]) -> bool:
    """
    Check the list `xs` is contained in the list `ys`.

    Returns:
      Returns True when the list `xs` is contained, wholly and intact, anywhere within the list `ys`.

    Examples:
      >>> is_infix_of ([1,2], [1,2,3,4,5])
      True
      >>> is_infix_of ([3,4,5], [1,2,3,4,5])
      True
      >>> is_infix_of ([2,3,4], [1,2,3,4,5])
      True
      >>> is_infix_of ([42,3], [3,42,7,9])
      False
    """
    if len(xs) > len(ys):
        return False
    for i in range(len(ys) - len(xs) + 1):
        if xs == ys[i:i + len(xs)]:
            return True
    return False


def is_subsequence_of(xs: List[T], ys: List[T]) -> bool:
    """
    Check the all elements of the list `xs` occur in the list `ys`, in order.
    The elements do not have to occur consecutively.

    Examples:
      >>> is_subsequence_of (list("GHC"), list("The Glorious Haskell Compiler"))
      True
      >>> is_subsequence_of (list("adefghi"), list("abcdefghi"))
      True
      >>> is_subsequence_of (list(range(1,10)), reverse(list(range(11))))
      False
    """
    i: int = 0
    for x in xs:
        for j, y in enumerate(ys[i:]):
            if x == y:
                i += j + 1
                break
        else:
            return False
    return True


def lookup(p: Predicate[T], xs: List[Tuple[T, U]]) -> Found[U]:
    """
    Search an element satisfy `p` and returns the associated element.

    Examples:
      >>> lookup (lambda x: x > 2, [(1,"one"), (2,"two"), (3,"three"), (4,"four")])
      Found('three')
      >>> n = lookup (lambda x: x < 0, [(1,"one"), (2,"two"), (3,"three"), (4,"four")])
      >>> if not(n):
      ...     print('not found x (< 0)')
      not found x (< 0)
    """
    for x, y in xs:
        if p(x):
            return Found.found(y)
    return Found.not_found(p)


def find(p: Predicate[T], xs: List[T]) -> Found[T]:
    """
    Search a value in the list `xs` from left to right.
    The value satisfies the predicate `p`.

    Returns:
      The value found in the list `xs`.
      Or if no values satisfies `p`, returns `NotFound`.

    Examples:
      >>> find (lambda x: x == 1, [1,2,3])
      Found(1)
      >>> find (lambda x: x == 42, [41,42,43])
      Found(42)
      >>> str(find (lambda x: x == 5, [0,2,4,6,8,10]))[:8]
      'NotFound'
      >>> m = find (lambda x: x == False, [False])
      >>> if m:
      ...     print('found False')
      found False
    """
    for x in xs:
        if p(x):
            return Found.found(x)
    return Found.not_found(p)


# pylint: disable-next=redefined-builtin
def filter(p: Predicate[T], xs: List[T]) -> List[T]:
    """
    Filter out elements from the list `xs` that do not satisfy the predicate `p` .

    Returns:
      List of elements satisfy `p`.

    Examples:
      >>> filter (lambda x: x % 2 == 0, list(range(10)))
      [0, 2, 4, 6, 8]
    """
    ys: List[T] = []
    for x in xs:
        if p(x):
            ys.append(x)
    return ys


def partition(p: Predicate[T], xs: List[T]) -> Tuple[List[T], List[T]]:
    """
    Partition the list `xs` into a tuple of 2 lists.
    All elements of the first list satisfy `p` and all elements of the second list do not satisfy `p`.

    Returns:
      A pair of lists of elements which do and do not satisfy the predicate `p`.

    Examples:
      >>> partition(lambda x: x < 4, [0, 3, 1, 4, 6, 5, 2])
      ([0, 3, 1, 2], [4, 6, 5])
      >>> partition(lambda x: x < 0, [0, 3, 1, 4, 6, 5, 2])
      ([], [0, 3, 1, 4, 6, 5, 2])
      >>> partition(lambda x: x%2==0, [0, 3, 1, 4, 6, 5, 2])
      ([0, 4, 6, 2], [3, 1, 5])
    """
    ys: List[T] = []
    zs: List[T] = []
    for x in xs:
        if p(x):
            ys.append(x)
        else:
            zs.append(x)
    return (ys, zs)


def elem_index(e: T, xs: List[T]) -> Found[int]:
    """
    Lookup the value `e` from the list `xs`, returns it's index.

    Returns:
      Returns index of the first element equals to `e` in `xs`.
      If it is not found in the list, `NotFound` is returned.

    Examples:
      >>> elem_index (3, [1,2,3,4])
      Found(2)
      >>> elem_index ("apple", ["orange", "banana"])
      NotFound('apple')
    """
    for i, x in enumerate(xs):
        if x == e:
            return Found.found(i)
    return Found.not_found(e)


def elem_indicies(e: T, xs: List[T]) -> List[int]:
    """
    Lookup all elements equal to the value `e` from the list `xs`, returns theirs indicies in ascending order.

    Returns:
      Returns all indicies of all elements equal to `e` in `xs`.

    Examples:
      >>> elem_indicies (3, [1,2,3,4,3,5,3])
      [2, 4, 6]
      >>> elem_indicies ("apple", ["orange", "banana"])
      []
    """
    res: List[int] = []
    for i, x in enumerate(xs):
        if x == e:
            res.append(i)
    return res


def find_index(p: Predicate[T], xs: List[T]) -> Found[int]:
    """
    Lookup the first element that satisfies the predicate `p` in the list `xs`, returns it's index.

    Returns:
      The index of the first value in the list `xs` that satisfies `p`.
      If no element satisfying `p`, returns `NotFound`.

    Examples:
      >>> find_index (lambda x: x > 3, [1, 3, 5, 7])
      Found(2)
      >>> str(find_index (lambda x: x < 10, [10, 15, 42, 777]))[:8]
      'NotFound'

    Example:
      The found value can be retrieved by `Found.unwrap <basic_iter.found.Found.unwrap>`.

      >>> find_index (lambda x: x > 40, [12, 22, 32, 42]).unwrap()
      3
    """
    for i, x in enumerate(xs):
        if p(x):
            return Found.found(i)
    return Found.not_found(p)


def find_indicies(p: Predicate[T], xs: List[T]) -> List[int]:
    """
    Lookup all elements that satisfy the predicate `p` in the list `xs`, returns their indicies.

    Returns:
      The list of indicies of all elements satisfy `p` in the list `xs`.

    Examples:
      >>> find_indicies (lambda x: x > 3, [1, 3, 5, 7, 5, 3, 1])
      [2, 3, 4]
      >>> find_indicies (lambda x: x < 10, [10, 15, 42, 777])
      []
    """
    res: List[int] = []
    for i, x in enumerate(xs):
        if p(x):
            res.append(i)
    return res


# pylint: disable-next=redefined-builtin
def zip(xs: List[T], ys: List[U]) -> List[Tuple[T, U]]:
    """
    Equivalent to calling `zip_with` on a tuple constructor like :code:`lambda x,y: (x,y)`.

    Examples:
      >>> zip([1,2,3], [4,5,6])
      [(1, 4), (2, 5), (3, 6)]

    Raises:
      AssertionError: `xs` and `ys` have different lengths.
    """
    return zip_with(lambda x, y: (x, y), xs, ys)


def zip3(xs: List[T], ys: List[U], zs: List[S]) -> List[Tuple[T, U, S]]:
    """
    Equivalent to calling `zip_with3` on a tuple constructor like :code:`lambda x,y,z: (x,y,z)`.

    Examples:
      >>> zip3([1,2,3], [4,5,6], [7,8,9])
      [(1, 4, 7), (2, 5, 8), (3, 6, 9)]

    Raises:
      AssertionError: `xs`, `ys` and `zs` do not have same lengths.
    """
    return zip_with3(lambda x, y, z: (x, y, z), xs, ys, zs)


def zip4(t1: List[T1], t2: List[T2], t3: List[T3], t4: List[T4]) -> List[Tuple[T1, T2, T3, T4]]:
    """
    Equivalent to calling `zip_with4` on a tuple constructor like :code:`lambda a,b,c,d: (a,b,c,d)`.

    Examples:
      >>> zip4([1,2,3], [4,5,6], [7,8,9], [10,11,12])
      [(1, 4, 7, 10), (2, 5, 8, 11), (3, 6, 9, 12)]

    Raises:
      AssertionError: `t1`, `t2`, `t3` and `t4` do not have same lengths.
    """
    return zip_with4(lambda a, b, c, d: (a, b, c, d), t1, t2, t3, t4)


def zip5(t1: List[T1], t2: List[T2], t3: List[T3], t4: List[T4], t5: List[T5]) -> List[Tuple[T1, T2, T3, T4, T5]]:
    """
    Equivalent to calling `zip_with5` on a tuple constructor like :code:`lambda a,b,c,d,e: (a,b,c,d,e)`.

    Examples:
      >>> zip5([1,2,3], [4,5,6], [7,8,9], [10,11,12], [13,14,15])
      [(1, 4, 7, 10, 13), (2, 5, 8, 11, 14), (3, 6, 9, 12, 15)]

    Raises:
      AssertionError: `t1`, `t2`, `t3`, `t4` and `t5` do not have same lengths.
    """
    return zip_with5(lambda a, b, c, d, e: (a, b, c, d, e), t1, t2, t3, t4, t5)


def zip6(t1: List[T1], t2: List[T2], t3: List[T3], t4: List[T4], t5: List[T5],
         t6: List[T6]) -> List[Tuple[T1, T2, T3, T4, T5, T6]]:
    """
    Equivalent to calling `zip_with6` on a tuple constructor like :code:`lambda a,b,c,d,e,f: (a,b,c,d,e,f)`.

    Examples:
      >>> zip6([1,2,3], [4,5,6], [7,8,9], [10,11,12], [13,14,15], [16,17,18])
      [(1, 4, 7, 10, 13, 16), (2, 5, 8, 11, 14, 17), (3, 6, 9, 12, 15, 18)]

    Raises:
      AssertionError: `t1`, `t2`, `t3`, `t4`, `t5` and `t6` do not have same lengths.
    """
    return zip_with6(lambda a, b, c, d, e, f: (a, b, c, d, e, f), t1, t2, t3, t4, t5, t6)


def zip7(
    t1: List[T1],
    t2: List[T2],
    t3: List[T3],
    t4: List[T4],
    t5: List[T5],
    t6: List[T6],
    t7: List[T7],
) -> List[Tuple[T1, T2, T3, T4, T5, T6, T7]]:
    """
    Equivalent to calling `zip_with7` on a tuple constructor like :code:`lambda a,b,c,d,e,f,g: (a,b,c,d,e,f,g)`.

    Examples:
      >>> zip7([1,2,3], [4,5,6], [7,8,9], [10,11,12], [13,14,15], [16,17,18], [19,20,21])
      [(1, 4, 7, 10, 13, 16, 19), (2, 5, 8, 11, 14, 17, 20), (3, 6, 9, 12, 15, 18, 21)]

    Raises:
      AssertionError: `t1`, `t2`, `t3`, `t4`, `t5`, `t6` and `t7` do not have same lengths.
    """
    return zip_with7(lambda a, b, c, d, e, f, g: (a, b, c, d, e, f, g), t1, t2, t3, t4, t5, t6, t7)


def zip_with(f: Callable[[T, U], S], xs: List[T], ys: List[U]) -> List[S]:
    """
    Returns:
      A Zipped list from lists `xs` and `ys` by the function `f`.

    Raises:
      AssertionError: `xs` and `ys` have different lengths.

    Examples:
      >>> zip_with (lambda x, y: x + y, [1,2,3], [4,5,6])
      [5, 7, 9]
      >>> import re
      >>> zip_with (lambda r,p: re.search(r,p) is None
      ...         , [r'abc',r'^192',r'txt$'], ['ABC','192.168.1.1','note.txt'])
      [True, False, False]
    """
    assert len(xs) == len(ys), "required to be the same length"
    itx = xs
    ity = ys
    res: List[S] = []
    while itx:
        x = itx[0]
        y = ity[0]
        itx = itx[1:]
        ity = ity[1:]
        res.append(f(x, y))
    return res


def zip_with3(f: Callable[[T1, T2, T3], S], t1: List[T1], t2: List[T2], t3: List[T3]) -> List[S]:
    """
    Returns:
      A Zipped list from lists `t1`, `t2` and `t3` by the function `f`.

    Raises:
      AssertionError: `t1`, `t2` and `t3` not have same lengths.

    Examples:
      >>> zip_with3(lambda x,y,z: x+y+z, [1,2,3], [4,5,6], [7,8,9])
      [12, 15, 18]
    """
    assert len(t1) == len(t2) == len(t3), "required to be the same length"
    it1, it2, it3 = (t1, t2, t3)
    res: List[S] = []
    while it1:
        a, b, c = (it1[0], it2[0], it3[0])
        it1, it2, it3 = (it1[1:], it2[1:], it3[1:])
        res.append(f(a, b, c))
    return res


def zip_with4(
    f: Callable[[T1, T2, T3, T4], S],
    t1: List[T1],
    t2: List[T2],
    t3: List[T3],
    t4: List[T4],
) -> List[S]:
    """
    Returns:
      A Zipped list from lists `t1`, `t2`, `t3` and `t4` by the function `f`.

    Raises:
      AssertionError: `t1`, `t2`, `t3` and `t4` not have same lengths.

    Examples:
      >>> zip_with4(lambda w,x,y,z: w+x+y+z, [1,2,3], [4,5,6], [7,8,9], [10,11,12])
      [22, 26, 30]
    """
    assert len(t1) == len(t2) == len(t3) == len(t4), "required to be the same length"
    it1, it2, it3, it4 = (t1, t2, t3, t4)
    res: List[S] = []
    while it1:
        a, b, c, d = (it1[0], it2[0], it3[0], it4[0])
        it1, it2, it3, it4 = (it1[1:], it2[1:], it3[1:], it4[1:])
        res.append(f(a, b, c, d))
    return res


def zip_with5(
    f: Callable[[T1, T2, T3, T4, T5], S],
    t1: List[T1],
    t2: List[T2],
    t3: List[T3],
    t4: List[T4],
    t5: List[T5],
) -> List[S]:
    """
    Returns:
      A Zipped list from lists `t1`, `t2`, `t3`, `t4` and `t5` by the function `f`.

    Raises:
      AssertionError: `t1`, `t2`, `t3`, `t4` and `t5` do not have same lengths.

    Examples:
      >>> zip_with5(lambda a,b,c,d,e: a+b+c+d+e, [1,2,3], [4,5,6], [7,8,9], [10,11,12], [13,14,15])
      [35, 40, 45]
    """
    assert (len(t1) == len(t2) == len(t3) == len(t4) == len(t5)), "required to be the same length"
    it1, it2, it3, it4, it5 = (t1, t2, t3, t4, t5)
    res: List[S] = []
    while it1:
        a, b, c, d, e = (it1[0], it2[0], it3[0], it4[0], it5[0])
        it1, it2, it3, it4, it5 = (it1[1:], it2[1:], it3[1:], it4[1:], it5[1:])
        res.append(f(a, b, c, d, e))
    return res


def zip_with6(
    t: Callable[[T1, T2, T3, T4, T5, T6], S],
    t1: List[T1],
    t2: List[T2],
    t3: List[T3],
    t4: List[T4],
    t5: List[T5],
    t6: List[T6],
) -> List[S]:
    """
    Returns:
      A Zipped list from lists `t1`, `t2`, `t3`, `t4`, `t5` and `t6` by the function `t`.

    Raises:
      AssertionError: `t1`, `t2`, `t3`, `t4`, `t5` and `t6` do not have same lengths.

    Examples:
      >>> zip_with6(lambda a,b,c,d,e,f: a+b+c+d+e+f, [1,2,3], [4,5,6], [7,8,9], [10,11,12], [13,14,15], [16,17,18])
      [51, 57, 63]
    """
    assert (len(t1) == len(t2) == len(t3) == len(t4) == len(t5) == len(t6)), "required to be the same length"
    it1, it2, it3, it4, it5, it6 = (t1, t2, t3, t4, t5, t6)
    res: List[S] = []
    while it1:
        a, b, c, d, e, f = (it1[0], it2[0], it3[0], it4[0], it5[0], it6[0])
        it1, it2, it3, it4, it5, it6 = (
            it1[1:],
            it2[1:],
            it3[1:],
            it4[1:],
            it5[1:],
            it6[1:],
        )
        res.append(t(a, b, c, d, e, f))
    return res


def zip_with7(
    t: Callable[[T1, T2, T3, T4, T5, T6, T7], S],
    t1: List[T1],
    t2: List[T2],
    t3: List[T3],
    t4: List[T4],
    t5: List[T5],
    t6: List[T6],
    t7: List[T7],
) -> List[S]:
    """
    Returns:
      A Zipped list from lists `t1`, `t2`, `t3`, `t4`, `t5`, `t6` and `t7` by the function `t`.

    Raises:
      AssertionError: `t1`, `t2`, `t3`, `t4`, `t5`, `t6` and `t7` do not have same lengths.

    Examples:
      >>> zip_with7(lambda a,b,c,d,e,f,g: a+b+c+d+e+f+g,
      ... [1,2,3], [4,5,6], [7,8,9], [10,11,12], [13,14,15], [16,17,18], [19,20,21])
      [70, 77, 84]
    """
    assert (len(t1) == len(t2) == len(t3) == len(t4) == len(t5) == len(t6) == len(t7)), "required to be the same length"
    it1, it2, it3, it4, it5, it6, it7 = (t1, t2, t3, t4, t5, t6, t7)
    res: List[S] = []
    while it1:
        a, b, c, d, e, f, g = (it1[0], it2[0], it3[0], it4[0], it5[0], it6[0], it7[0])
        it1, it2, it3, it4, it5, it6, it7 = (
            it1[1:],
            it2[1:],
            it3[1:],
            it4[1:],
            it5[1:],
            it6[1:],
            it7[1:],
        )
        res.append(t(a, b, c, d, e, f, g))
    return res


def unzip(xs: List[Tuple[T1, T2]]) -> Tuple[List[T1], List[T2]]:
    """
    Transforms the list of pairs `xs` into a list of first elements and second elements.

    Examples:
      >>> unzip([(0,1),(2,3),(4,5)])
      ([0, 2, 4], [1, 3, 5])
    """
    ts1: List[T1] = []
    ts2: List[T2] = []
    for t1, t2 in xs:
        ts1.append(t1)
        ts2.append(t2)
    return (ts1, ts2)


def unzip3(xs: List[Tuple[T1, T2, T3]]) -> Tuple[List[T1], List[T2], List[T3]]:
    """
    Transforms the list of tuples `xs` into a tuple of lists of n-th elements.

    Examples:
      >>> unzip3([(0,1,2),(3,4,5),(5,6,7)])
      ([0, 3, 5], [1, 4, 6], [2, 5, 7])
    """
    ts1: List[T1] = []
    ts2: List[T2] = []
    ts3: List[T3] = []
    for t1, t2, t3 in xs:
        ts1.append(t1)
        ts2.append(t2)
        ts3.append(t3)
    return (ts1, ts2, ts3)


def unzip4(xs: List[Tuple[T1, T2, T3, T4]]) -> Tuple[List[T1], List[T2], List[T3], List[T4]]:
    """
    Transforms the list of tuples `xs` into a tuple of lists of n-th elements.

    Examples:
      >>> unzip4([(0,1,2,3),(1,2,3,4),(2,3,4,5),(3,4,5,6)])
      ([0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6])
    """
    ts1: List[T1] = []
    ts2: List[T2] = []
    ts3: List[T3] = []
    ts4: List[T4] = []
    for t1, t2, t3, t4 in xs:
        ts1.append(t1)
        ts2.append(t2)
        ts3.append(t3)
        ts4.append(t4)
    return (ts1, ts2, ts3, ts4)


def unzip5(xs: List[Tuple[T1, T2, T3, T4, T5]]) -> Tuple[List[T1], List[T2], List[T3], List[T4], List[T5]]:
    """
    Transforms the list of tuples `xs` into a tuple of lists of n-th elements.

    Examples:
      >>> unzip5([(0,1,2,3,4),(1,2,3,4,5),(2,3,4,5,6),(3,4,5,6,7)])
      ([0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7])
    """
    ts1: List[T1] = []
    ts2: List[T2] = []
    ts3: List[T3] = []
    ts4: List[T4] = []
    ts5: List[T5] = []
    for t1, t2, t3, t4, t5 in xs:
        ts1.append(t1)
        ts2.append(t2)
        ts3.append(t3)
        ts4.append(t4)
        ts5.append(t5)
    return (ts1, ts2, ts3, ts4, ts5)


def unzip6(
        xs: List[Tuple[T1, T2, T3, T4, T5, T6]]) -> Tuple[List[T1], List[T2], List[T3], List[T4], List[T5], List[T6]]:
    """
    Transforms the list of tuples `xs` into a tuple of lists of n-th elements.

    Examples:
      >>> unzip6([(0,1,2,3,4,5),(1,2,3,4,5,6),(2,3,4,5,6,7),(3,4,5,6,7,8)])
      ([0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8])
    """
    ts1: List[T1] = []
    ts2: List[T2] = []
    ts3: List[T3] = []
    ts4: List[T4] = []
    ts5: List[T5] = []
    ts6: List[T6] = []
    for t1, t2, t3, t4, t5, t6 in xs:
        ts1.append(t1)
        ts2.append(t2)
        ts3.append(t3)
        ts4.append(t4)
        ts5.append(t5)
        ts6.append(t6)
    return (ts1, ts2, ts3, ts4, ts5, ts6)


def unzip7(
    xs: List[Tuple[T1, T2, T3, T4, T5, T6, T7]]
) -> Tuple[List[T1], List[T2], List[T3], List[T4], List[T5], List[T6], List[T7]]:
    """
    Transforms the list of tuples `xs` into a tuple of lists of n-th elements.

    Examples:
      >>> unzip7([(0,1,2,3,4,5,6),(1,2,3,4,5,6,7),(2,3,4,5,6,7,8),(3,4,5,6,7,8,9)])
      ([0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8], [6, 7, 8, 9])
    """
    ts1: List[T1] = []
    ts2: List[T2] = []
    ts3: List[T3] = []
    ts4: List[T4] = []
    ts5: List[T5] = []
    ts6: List[T6] = []
    ts7: List[T7] = []
    for t1, t2, t3, t4, t5, t6, t7 in xs:
        ts1.append(t1)
        ts2.append(t2)
        ts3.append(t3)
        ts4.append(t4)
        ts5.append(t5)
        ts6.append(t6)
        ts7.append(t7)
    return (ts1, ts2, ts3, ts4, ts5, ts6, ts7)


def lines(ss: str) -> List[str]:
    """
    Split the given string delimited by line break character.

    Examples:
      >>> lines('')
      []
      >>> lines('\\n')
      ['']
      >>> lines('one')
      ['one']
      >>> lines('one\\n')
      ['one']
      >>> lines('one\\n\\n')
      ['one', '']
      >>> lines('one\\ntwo')
      ['one', 'two']
      >>> lines('one\\ntwo\\n')
      ['one', 'two']
    """
    return str.splitlines(ss)


def words(ss: str) -> List[str]:
    """
    Split the given string delimited by line break character.

    Examples:
      >>> words('')
      []
      >>> words(' ')
      []
      >>> words('one')
      ['one']
      >>> words('one ')
      ['one']
      >>> words('one  ')
      ['one']
      >>> words('one two')
      ['one', 'two']
      >>> words('one two ')
      ['one', 'two']
    """
    res: List[str] = []
    sep: bool = True
    for c in ss:
        if c == " ":
            sep = True
        else:
            if sep:
                res.append("")
                sep = False
            res[-1] += c

    return res


def unlines(ss: List[str]) -> str:
    """
    It joins lines, after appending a terminating newline to each.

    Examples:
      >>> unlines([])
      ''
      >>> unlines(["foo", "bar", "baz"])
      'foo\\nbar\\nbaz\\n'
    """
    return "".join(s + "\n" for s in ss)


def unwords(ss: List[str]) -> str:
    """
    It joins words with separating spaces.

    Examples:
      >>> unwords([])
      ''
      >>> unwords(["foo", "bar", "baz"])
      'foo bar baz'
    """
    return " ".join(ss)


def nub(xs: List[T]) -> List[T]:
    """
    Removes duplicate elements from the list `xs`.
    It keeps only the first occurrence of each element.

    Examples:
      >>> nub(list("abcabc"))
      ['a', 'b', 'c']
      >>> nub([5,3,1,3,5])
      [5, 3, 1]
    """
    res: List[T] = []
    for x in xs:
        if not x in res:
            res.append(x)
    return res


def delete(x: T, xs: List[T]) -> List[T]:
    """
    Removes the first occurrence of `x` from the list `xs`.

    Returns:
      List with the first occurrence of `x` removed.

    Examples:
      >>> delete ('a', list("banana"))
      ['b', 'n', 'a', 'n', 'a']
      >>> delete (1, [2,3,1,4])
      [2, 3, 4]
    """
    for i, e in enumerate(xs):
        if e == x:
            return xs[0:i] + xs[i + 1:]
    return xs


def delete_firsts(xs: List[T], ys: List[T]) -> List[T]:
    """
    Remove each element of `ys` from `xs`.
    Equals to `(\\\\\\\\) in Haskell <https://hackage.haskell.org/package/base-4.10.1.0/docs/Data-List.html#v:-92--92->`_.

    Examples:
      >>> delete_firsts ([1,2,3,4,5], [1,2,3])
      [4, 5]
      >>> delete_firsts ([1,2,3,4,5], [3,5])
      [1, 2, 4]
      >>> delete_firsts ([1,2,3], [1,2,3,4,5])
      []
      >>> delete_firsts (list("banana"), list("nana"))
      ['b', 'a']
    """
    res: List[T] = xs
    for y in ys:
        res = delete(y, res)
    return res


def union(xs: List[T], ys: List[T]) -> List[T]:
    """
    Construct a list from all elements in `xs` and all elements in `ys` that are not exist in `xs`.

    Examples:
      >>> union([1,2,3], [1,2])
      [1, 2, 3]
      >>> union([1,2,3,3], [1,2])
      [1, 2, 3, 3]
      >>> union([1,2,3], [1,2,2])
      [1, 2, 3]
    """
    gys: Generator[T, None, None] = (y for y in ys)
    return xs + list(foldl(lambda acc, e: (x for x in acc if e != x), gys, xs))


def intersect(xs: List[T], ys: List[T]) -> List[T]:
    """
    The intersection of `xs` and `ys`.
    But `xs` contains duplicates, so will the result.

    Examples:
      >>> intersect([1,2,3,4], [2,4,6,8])
      [2, 4]
      >>> intersect([1,2,2,3,4], [6,4,4,2])
      [2, 2, 4]
    """
    return filter(lambda x: x in ys, xs)


def nub_by(eq: Callable[[T, T], bool], xs: List[T]) -> List[T]:
    """
    Generalized `nub` by the user equality predicate `eq`.

    Examples:
      >>> nub_by(lambda x,y: x.upper() == y.upper(), list("abcABC"))
      ['a', 'b', 'c']
      >>> nub_by(lambda x,y: x%3 == y%3, [5,3,1,3,5])
      [5, 3, 1]
    """
    res: List[T] = []
    for x in xs:
        # pylint: disable-next=cell-var-from-loop
        if all(lambda e: not eq(e, x), res):
            res.append(x)
    return res


def delete_by(eq: Callable[[T, T], bool], x: T, xs: List[T]) -> List[T]:
    """
    Behaves like `delete` except for taking user equality predicate `eq`.

    Returns:
      List with the first occurrence of `x` removed.

    Examples:
      >>> delete_by (lambda x,y: x.lower() == y.lower(), 'a', list("bAnAna"))
      ['b', 'n', 'A', 'n', 'a']
      >>> delete_by (lambda x,y: x == y, 1, [2,3,1,4])
      [2, 3, 4]
    """
    for i, e in enumerate(xs):
        if eq(e, x):
            return xs[0:i] + xs[i + 1:]
    return xs


def delete_firsts_by(eq: Callable[[T, T], bool], xs: List[T], ys: List[T]) -> List[T]:
    """
    The list `xs` with the first occurrence of each element of the list `ys` removed.

    Examples:
      >>> delete_firsts_by(lambda x,y: x%7==y%7, [1,2,7,8,9], [9,9,9])
      [1, 7, 8]
      >>> delete_firsts_by(lambda x,y: x[0]==y[0], [("foo",1),("bar",2),("foo",42)], [("bar",3), ("foo",5)])
      [('foo', 42)]
    """
    res: List[T] = xs
    for y in ys:
        res = delete_by(eq, y, res)
    return res


def union_by(eq: Callable[[T, T], bool], xs: List[T], ys: List[T]) -> List[T]:
    """
    Generalized `union` by the user defined equality predicate `eq`.

    Examples:
      >>> group_mod3 = lambda x,y: x%3 == y%3
      >>> union_by(group_mod3, [1,2,3], [4,8])
      [1, 2, 3]
      >>> union_by(group_mod3, [1,32,33,3], [1,2])
      [1, 32, 33, 3]
      >>> union_by(group_mod3, [28,2,12], [1,2,2])
      [28, 2, 12]
    """
    gys: Generator[T, None, None] = (y for y in ys)
    return xs + list(foldl(lambda acc, e: (x for x in acc if not eq(e, x)), gys, xs))


def intersect_by(eq: Callable[[T, T], bool], xs: List[T], ys: List[T]) -> List[T]:
    """
    Generalized `intersect` by the user defined equality predicate `eq`.

    Examples:
      >>> group_mod3 = lambda x,y: x%3 == y%3
      >>> intersect_by(group_mod3, [1,2,3,4], [2,4,6,8])
      [1, 2, 3, 4]
      >>> intersect_by(group_mod3, [1,2,2,3,4], [6,12,0])
      [3]
    """
    return filter(lambda x: find(lambda e: eq(e, x), ys).is_found, xs)


def group_by(f: Callable[[T, T], bool], xs: List[T]) -> List[List[T]]:
    """
    All the elememts of `xs` are grouped into each lis by the binary predicate `f`.
    In each group, the predicate `f` holds for all adjacent elements.

    Return:
      List[List[T]]:
        A list of group of elements which are grouped by the predicate `f`.

    Examples:
      >>> group_by (lambda x,y: x == y, [1,1,1,2,2,3,3,3,3])
      [[1, 1, 1], [2, 2], [3, 3, 3, 3]]
      >>> group_by (lambda x,y: x == y, [])
      []
      >>> group_by (lambda x,y: x <= y, [1,2,2,3,1,2,0,4,5,2])
      [[1, 2, 2, 3], [1, 2], [0, 4, 5], [2]]
      >>> group_by (is_prefix_of, ['a','ab','abra','ra','racata','racatabra'])
      [['a', 'ab', 'abra'], ['ra', 'racata', 'racatabra']]
    """
    if null(xs):
        return []

    gs: List[List[T]] = [[xs[0]]]
    for x in xs[1:]:
        if f(gs[-1][-1], x):
            gs[-1].append(x)
        else:
            gs.append([x])
    return gs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
