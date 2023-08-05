"""
Module that implements :class:`Document` class representing a text document as token sequence.
.. codeauthor:: Philip Paprotny <philip.paprotny@gmail.com>
"""

from typing import Dict, Union, List, Callable, Optional, Any, Iterable, Set, Tuple, Sequence, Collection, TypeVar, cast

class Document:
    """
    A class that represents text as sequence of tokens. Attributes are also implemented at two levels:
    1. Document attributes like the document label and analysis results;
    2. Token attributes (e.g. POS, lemma, etc.)
    """
    def __init__(self, label: str, doc_attrs: Optional[Dict[str, Any]] = None):
        """
        Create a new :class:`~nlpp.corpus.Document` object.
        """
        # set up document attributes
        doc_attrs = {} if doc_attrs is None else doc_attrs.copy()
        self.doc_attrs = doc_attrs

    def __len__(self) -> int:
        """
        Length of the document, i.e. number of tokens.
        :return: length of the document, i.e. number of tokens
        """
        return 0

    def __repr__(self) -> str:
        """
        Document summary.
        :return: document summary as string
        """
        return f'Document "{self.label}" ({len(self)} tokens, {len(self.doc_attrs)} document attributes)'

    def __str__(self) -> str:
        """
        Document summary.
        :return: document summary as string
        """
        return self.__repr__()

    @property
    def label(self) -> str:
        """Document label (document name)."""
        return self.doc_attrs['label']
