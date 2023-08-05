"""
Module that implements :class:`Corpus` class representing a set of texts as token sequences in labelled
documents.
.. codeauthor:: Philip Paprotny <philip.paprotny@gmail.com>
"""
import glob
import logging

from spacy.tokens import Doc, Token
from nlpp.model.document import Document

log = logging.getLogger(__name__)

# set custom annotations
Doc.set_extension("title", default=False)
Doc.set_extension("analysis", default={})
Token.set_extension("timestamp", default=None)


class Corpus:
    """
    The Corpus class represents text as *spaCy Docs* in labelled documents. It behaves like a Python dict,
    i.e. you can access document tokens via square brackets (``corp['my_doc']``).
	"""

    def __init__(self, docs):
        self._docs = docs

    @property
    def docs(self):
        return self._docs

    def __getitem__(self, x):
        if isinstance(x, int):
            print(f"Document: {self._docs[x]._.title} | Analysis: {self._docs[x]._.analysis}")
            return self._docs[x]
        if isinstance(x, str):
            for i, doc in enumerate(self._docs):
                if doc._.title == x:
                    return self._docs[i]
                else:
                    raise ValueError("Title not in Corpus.")
        else:
            return

    def __iter__(self):
        i=0
        max = len(self._docs)
        while i < max:
            yield self._docs[i]
            i+=1

    def add_file(self, path_file, title):
        # subs = Corpus.parse_subtitle(path_file)
        doc = Document._init_document(path_file, title)
        self._docs.append(doc)

    def export_as_csv(self, path_file):
        pass

    @classmethod
    def from_subs(cls, path_folder, titles):
        paths = glob.glob(f"{path_folder}/*.srt")
        paths.sort()
        res = []

        for i, path in enumerate(paths):
            res_doc = Document._init_document_from_sub(path, titles[i])
            res.append(res_doc)

        log.info(f"created Corpus of subtitles from folder: {path_folder}")

        return cls(res)

