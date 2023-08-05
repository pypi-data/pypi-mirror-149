import logging
import spacy

from spacy.tokens import Doc
from nlpp.parser import Parser

log = logging.getLogger(__name__)

# # set custom annotations
# Doc.set_extension("title", default=False)
# Doc.set_extension("analysis", default={})
# Token.set_extension("timestamp", default=None)

nlp = spacy.load("en_core_web_sm")

class Document(Doc):

    @classmethod
    def _init_document_from_sub(cls, path, title):
        print(f"adding {title} to corpus from file: ")
        print(f"{path}\n")

        subs = cls.parse_subtitle(path)
        subs_text = [i.text for i in subs]
        temp_docs = list(nlp.pipe(subs_text))
        cls.add_timestamps(temp_docs, subs)

        res_doc = cls.from_docs(temp_docs)
        res_doc._.title = title
        log.info(f"Added file: {path} to corpus with title: {title}")
        return res_doc

    @staticmethod
    def add_timestamps(temp_docs, subs):
        for sub, doc in zip(subs, temp_docs):
            for token in doc:
                token._.timestamp = sub.start

    @staticmethod
    def parse_subtitle(path_file):
        p = Parser("text")
        subs = list(p.from_sub(path_file))
        return subs
