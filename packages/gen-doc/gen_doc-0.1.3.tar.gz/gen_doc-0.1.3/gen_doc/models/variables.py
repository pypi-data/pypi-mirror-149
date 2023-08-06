"""
Additional entities
"""
# pylint: disable=invalid-name
from enum import Enum


class EnumTypeVariables(str, Enum):
    NONE = "none"
    BOOL = "bool"
    NUM = "num"
    STR = "str"
    OBJ = "object"
    NAME = "name"
    DICT = "dict"
    TUPLE = "tuple"
    LIST = "list"
    SET = "set"
    SLICE = "slice"
    BIN_OP = "bin_op"
    UNARY_OP = "unary_op"
    UNPARSE = "unparse"


class Operations(Enum):
    Div = "/"
    Add = "+"
    Sub = "-"
    Mult = "*"
    MatMult = "@"
    Mod = "%"
    Pow = "**"
    LShift = "<<"
    RShift = ">>"
    BitOr = "|"
    BitXor = "^"
    BitAnd = "&"
    FloorDiv = "//"
    USub = "-"
    UAdd = "+"
