"""
Module for functions that work with text represented as *token sequences*, e.g. ``["A", "test", "document", "."]``
and single tokens (i.e. strings).

.. codeauthor:: Philip Paprotny <philip.paprotny@gmail.com>
"""
from typing import Dict, Union, List, Callable, Optional, Any, Iterable, Set, Tuple, Sequence, Collection, TypeVar, cast

def unique_chars(tokens: Iterable[str]) -> Set[str]:
    """
    Return a set of all characters used in `tokens`.
    :param tokens: iterable of string tokens
    :return: set of all characters used in `tokens`
    """
    chars = set()
    for t in tokens:
        chars.update(set(t))
    return chars
