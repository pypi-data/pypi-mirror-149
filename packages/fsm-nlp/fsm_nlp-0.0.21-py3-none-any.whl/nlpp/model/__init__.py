"""
Module for processing text as token sequences in labelled documents. A set of documents is represented as *corpus*
using the :class:`Corpus` class. This sub-package also provides functions that work with a :class:`Corpus` object.
Text parsing and processing relies on the `SpaCy library <https://spacy.io/>`_ which must be installed when using this
sub-package.
.. codeauthor:: Philip Paprotny <philip.paprotny@gmail.com>
"""
from .corpus import Corpus
# from .corpus_funcs import ()
