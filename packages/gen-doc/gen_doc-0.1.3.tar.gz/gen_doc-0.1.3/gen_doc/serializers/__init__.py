"""
import serializers
"""
from enum import Enum

from .markdown import MarkdownSerializer
from .serializer import GenDocSerializer

GenDocSerializers = Enum(  # type: ignore
    "GenDocSerializers",
    {
        serializer.short_name: serializer
        for serializer in GenDocSerializer.__subclasses__()
    },
)
