"""
Internal module that implements functions that operate on :class:`~nlpp.corpus.Corpus` objects.
.. codeauthor:: Philip Paprotny <philip.paprotny@gmail.com>
"""
import sys
import logging
from typing import Dict, Union, List, Callable, Optional, Any, Iterable, Set, Tuple, Sequence, Collection, TypeVar, cast
from functools import wraps

from .corpus import Corpus

# logging block
logging.basicConfig(filename='nlpp.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s | %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.WARNING)
log.addHandler(handler)

def add(a, b):
    return a + b

def corp_func(docs: Corpus) -> Any:
    """
    Test func.
    """

def corpus_func_inplace_opt(fn: Callable) -> Callable:
    """
    Decorator for a Corpus function `fn` with an optional argument ``inplace``. This decorator makes sure that if
    `fn` is called with ``inplace=False``, the passed corpus will be copied before `fn` is applied to it. Then,
    the modified copy of corpus is returned. If ``inplace: bool = True``, `fn` is applied as usual.

    :param fn: Corpus function `fn` with an optional argument ``inplace``
    :return: wrapper function of `fn`
    """
    # @wraps(fn)
    # def inner_fn(*args, **kwargs) -> Union[None, Corpus, Tuple[Corpus, Any]]:
    #     if not isinstance(args[0], Corpus):
    #         raise ValueError('first argument must be a Corpus object')

    #     if 'inplace' in kwargs:
    #         inplace = kwargs.pop('inplace')
    #     else:
    #         inplace = True

    #     # get Corpus object `corp`, optionally copy it
    #     if inplace:
    #         logger.debug(f'applying function {str(fn)} to {str(args[0])} inplace')
    #         corp = args[0]
    #     else:
    #         logger.debug(f'applying function {str(fn)} to a copy of {str(args[0])}')
    #         corp = copy(args[0])   # copy of this Corpus, a new object with same data but the *same* SpaCy instance

    #     # apply fn to `corp`, passing all other arguments
    #     ret = fn(corp, *args[1:], **kwargs)
    #     if ret is None:         # most Corpus functions return None
    #         if inplace:         # no need to return Corpus since it was modified in-place
    #             return None
    #         else:               # return the modified copy
    #             return corp
    #     else:                   # for Corpus functions that return something
    #         if inplace:
    #             return ret
    #         else:
    #             return corp, ret    # always return the modified Corpus copy first

    # return inner_fn
    return

@corpus_func_inplace_opt
def set_document_attr(docs: Corpus, attrname: str, data: Dict[str, Any], default: Optional[Any] = None,
                      inplace: bool = True) \
        -> Optional[Corpus]:
    """
    Set a document attribute named `attrname` for documents in Corpus object `docs`. If the attribute
    already exists, it will be overwritten.
    .. seealso:: See :func:`~tmtoolkit.corpus.remove_document_attr` to remove a document attribute.
    :param docs: a Corpus object
    :param attrname: name of the document attribute
    :param data: dict that maps document labels to document attribute value
    :param default: default document attribute value
    :param inplace: if True, modify Corpus object in place, otherwise return a modified copy
    :return: either None (if `inplace` is True) or a modified copy of the original `docs` object
    """

    pass
