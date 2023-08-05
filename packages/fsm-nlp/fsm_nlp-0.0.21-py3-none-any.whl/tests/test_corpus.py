"""
Tests for nlpp.corpus module including nlp.corpus_funcs.

.. codeauthor:: Philip Paprotny <philip.paprotny@gmail.com>
"""
import pytest
import os

import nlpp.model.corpus_funcs

DATADIR = os.path.join('tests', 'data')

def test_datadirs():
    assert os.path.exists(DATADIR)

def test_corpus_dummy():
    assert nlpp.model.corpus_funcs.add(2,3) == 5




