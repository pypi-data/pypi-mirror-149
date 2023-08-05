#%%
import os
from typing import Dict, Union, List, Callable, Optional, Any, Iterable, Set, Tuple, Sequence, Collection, TypeVar, cast

# import fitz
from pysubparser import parser as sub_parser

VALID_TYPES = {'text', 'blocks', 'words', 'html', 'dict', 'rawdict', 'rawjson', 'xhtml', 'xml'}

#%%
class Parser:
    """
    The Parser Class is the blueprint for all specific parsers.
	"""

    def __init__(self, parser_type: Optional[str] = None):
        """
        Create a new :class:`Parser` class.

        :param parser_type: type of parser

        self.parser_type = parser_type

        “text”: (default) plain text with line breaks. No formatting, no text position details, no images.
        “blocks”: generate a list of text blocks (= paragraphs).
        “words”: generate a list of words (strings not containing spaces).
        “html”: creates a full visual version of the page including any images. This can be displayed with your internet browser.
        “dict” / “json”: same information level as HTML, but provided as a Python dictionary or resp. JSON string. See TextPage.extractDICT() for details of its structure.
        “rawdict” / “rawjson”: a super-set of “dict” / “json”. It additionally provides character detail information like XML. See TextPage.extractRAWDICT() for details of its structure.
        “xhtml”: text information level as the TEXT version but includes images. Can also be displayed by internet browsers.
        “xml”: contains no images, but full position and font information down to each single text character. Use an XML module to interpret.
        """



    def __str__(self) -> str:
        """String representation of this Parser Object"""
        return self.__repr__()

    def __repr__(self) -> str:
        """String representation of this Parser Object"""
        return f'<Parser [type: {self.parser_type}]>'




    @property
    def parser_type(self) -> str:
        return self._parser_type

    @parser_type.setter
    def parser_type(self, parser_type):
        try:
            Parser.is_valid_type(parser_type)
            self._parser_type = parser_type

        except ValueError as e:
            print(e)

    @staticmethod
    def is_valid_type(parser_type):

        if parser_type is None:
            raise ValueError('Type is None. Please enter type ({VALID_TYPES}))')

        if parser_type in VALID_TYPES:
            return True
        else:
            raise ValueError(f'Type {parser_type} is not valid. Please enter type ({VALID_TYPES}))')

    # def from_pdf(self, file):
    #     test_file = '/home/philippy/youtube/00_tarantino_fucks/data/pulp-fiction-1994.pdf'
    #     file = test_file
    #     doc = fitz.open(file)

    #     res = [text for page in doc for text in page.get_text(self.parser_type)]
    #     # is equivalent to:
    #     # res = []
    #     # for page in doc:
    #         #   for text in page:
    #     #     res.append(page.get_text("blocks"))

    #     return res

    def from_sub(self, path):
        subtitles = sub_parser.parse(path)

        return subtitles
        # for subtitle in subtitles:
        #     print(f'{subtitle.start}\n{subtitle.text}')
# %%
# preview html
# import os
# import webbrowser

# p = Parser("html")
# html = f'<html>{"".join(p.from_pdf("test"))}</html>'

# path = os.path.abspath('temp.html')
# url = 'file://' + path

# with open(path, 'w') as f:
#     f.write(html)
# webbrowser.open(url)
