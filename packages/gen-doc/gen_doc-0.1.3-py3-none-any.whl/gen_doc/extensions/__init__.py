"""
import generators for extensions
"""

from enum import Enum

from .parser import GenDocParser
from .python import GenDocPythonParser

GenDocParsers = Enum(  # type: ignore
    "GenDocParsers",
    {parser.short_name: parser for parser in GenDocParser.__subclasses__()},
)
