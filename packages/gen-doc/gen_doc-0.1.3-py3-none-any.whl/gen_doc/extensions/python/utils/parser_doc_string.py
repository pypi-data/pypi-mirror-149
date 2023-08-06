"""
module with class py parsers doc string
"""
from typing import Optional

from gen_doc.models import ParsedDocString

from .parser_python_google_docstring import GoogleDocStringPyParser
from .parser_python_sphinx_docstring import SphinxDocStringPyParser


class DocStingPyParser:
    """
    Class parsers doc string
    """

    @staticmethod
    def parse(doc_string: Optional[str]) -> Optional[ParsedDocString]:
        """
        Method parse doc string and return
        :param doc_string: parsed doc string
        :type doc_string: str
        :return: parsed object
        :rtype: Optional[ParsedDocString]
        """
        if not doc_string:
            return None
        return max(
            [
                GoogleDocStringPyParser.parse(doc_string=doc_string),
                SphinxDocStringPyParser.parse(doc_string=doc_string),
            ]
        )
