"""
Module with python Sphinx docstrings parser
"""
import re
from typing import Dict, List, Optional, Tuple

from gen_doc.models import Parameter, ParsedDocString

from .base_parser import PythonDocStringParser
from .utils import strip_rows

GENERAL_STOPPERS = r"(?:(?=:param)|(?=:attr)|(?=:return)|(?=:yield)|(?=:note)|(?=:raises)|(?=:type)|(?=:rtype)|(?=:ytype)|(?=:todo)|(?=:example)|(?=\.\. code-block::)|\Z)"  # noqa

DESCRIPTION_REGEX = re.compile(
    # f"(?P<description_method>[.\*\w\s\d]+){GENERAL_STOPPERS}", re.S  # noqa
    f"(?P<description_method>.*?){GENERAL_STOPPERS}",
    re.S,  # noqa
)

PARAM_REGEX = re.compile(
    f":param (?P<param>[\*\w\s\[\]\,]+): (?P<param_doc>.*?){GENERAL_STOPPERS}",  # noqa
    re.S,  # noqa
)
ATTR_REGEX = re.compile(
    f":attr (?P<attr>[\*\w\s\[\]\,]+): (?P<attr_doc>.*?){GENERAL_STOPPERS}",  # noqa
    re.S,  # noqa
)
TYPE_REGEX = re.compile(
    f":type (?P<param>[\*\w\s]+): (?P<type>.*?){GENERAL_STOPPERS}", re.S  # noqa
)
RAISES_REGEX = re.compile(
    f":raises (?P<error_type>[\*\w\s]+): (?P<error_type_doc>.*?){GENERAL_STOPPERS}",  # noqa
    re.S,
)
NOTE_REGEX = re.compile(f":note:(?P<note_doc>.*?){GENERAL_STOPPERS}", re.S)  # noqa
TODO_REGEX = re.compile(f":todo:(?P<todo_doc>.*?){GENERAL_STOPPERS}", re.S)  # noqa
RETURNS_REGEX = re.compile(
    f":return:(?P<return_doc>.*?){GENERAL_STOPPERS}", re.S
)  # noqa
YIELD_REGEX = re.compile(f":yield:(?P<yield_doc>.*?){GENERAL_STOPPERS}", re.S)  # noqa
RETURN_TYPE_REGEX = re.compile(
    f":rtype: (?P<rtype>.*?){GENERAL_STOPPERS}", re.S
)  # noqa
YIELD_TYPE_REGEX = re.compile(f":ytype: (?P<ytype>.*?){GENERAL_STOPPERS}", re.S)  # noqa
EXAMPLE_REGEX = re.compile(
    f"\.\. code-block:: (?P<language>[\*\w\s]+)(?P<example>.*?){GENERAL_STOPPERS}",  # noqa
    re.S,
)
EXAMPLE_REGEX_2 = re.compile(
    f":example:(?P<example>.*?){GENERAL_STOPPERS}", re.S
)  # noqa


class SphinxDocStringPyParser(PythonDocStringParser):
    """
    Sphinx doc string parser
    """

    example = """
    Object doc string
    with long description

    :param value1: description to value1
    :type value1: str
    :param List[str] value2: description to value2
    long description value2
    :attr value3: description to value3
    :type value3: Dict[str, str]
    :attr List[Tuple[str, str]] value4: description to value3
    :return: what return function
    :rtype: type returned value
    :yield: if yield function
    :ytype: for yield value
    :note: note string
    with some information
    :todo: todo1
    :todo: todo2
    with description
    :example:
    >>> import this
    >>> # and other imports
    """

    @staticmethod
    def parse(doc_string: Optional[str]) -> Optional[ParsedDocString]:
        """Function to parse doc string to a standard object
        ! sphinx doc string style
        :param doc_string: received function doc string
        :type doc_string: str
        :return: parsed object
        :rtype:Optional[ParsedDocString]
        """

        def parse_params_type(
            _params: Dict[str, str], _types: Dict[str, str]
        ) -> Tuple[Dict[str, str], Dict[str, str]]:
            to_del = list()
            new = dict()
            for param, doc in _params.items():
                tmp = param.split()
                if len(tmp) > 1:
                    to_del.append(param)
                    new[tmp[-1]] = doc
                    _types[tmp[-1]] = " ".join(tmp[:-1])

            for to_delete in to_del:
                del _params[to_delete]
            _params.update(new)

            return _params, _types

        def convert_params_attrs(
            _vals: Dict[str, str], _types: Dict[str, str]
        ) -> List[Parameter]:
            _vals, _types = parse_params_type(_vals, _types)
            _values = [
                Parameter(
                    param_name=param,
                    param_type=_types.get(param, None),
                    param_description=strip_rows(doc),
                )
                for param, doc in _vals.items()
            ]
            return _values

        if not doc_string:
            return None
        params = {
            param: strip_rows(doc) for param, doc in PARAM_REGEX.findall(doc_string)
        }
        to_dos = [strip_rows(to_do) for to_do in TODO_REGEX.findall(doc_string)]
        attrs = {attr: strip_rows(doc) for attr, doc in ATTR_REGEX.findall(doc_string)}
        types = {
            param: strip_rows(_type) for param, _type, in TYPE_REGEX.findall(doc_string)
        }

        parameters = convert_params_attrs(params, types)
        attributes = convert_params_attrs(attrs, types)
        raises = [
            Parameter(param_type=error, param_description=strip_rows(doc))
            for error, doc in RAISES_REGEX.findall(doc_string)
        ]
        returns_match = RETURNS_REGEX.search(doc_string)
        returns = ""
        if returns_match:
            returns = strip_rows(returns_match.group("return_doc"))

        notes_match = NOTE_REGEX.search(doc_string)
        notes = ""
        if notes_match:
            notes = strip_rows(notes_match.group("note_doc"))
        returns_type_match = RETURN_TYPE_REGEX.search(doc_string)
        return_type = None
        if returns_type_match:
            return_type = strip_rows(returns_type_match.group("rtype"))
        yield_match = YIELD_REGEX.search(doc_string)
        yields = ""
        if yield_match:
            yields = strip_rows(yield_match.group("yield_doc"))
        yields_type_match = YIELD_TYPE_REGEX.search(doc_string)
        yield_type = None
        if yields_type_match:
            yield_type = strip_rows(yields_type_match.group("ytype"))

        match_ex = EXAMPLE_REGEX.search(doc_string)
        example = ""
        if match_ex:
            example = strip_rows(match_ex.group("example"))
        else:
            match_ex = EXAMPLE_REGEX_2.search(doc_string)
            if match_ex:
                example = strip_rows(match_ex.group("example"))
        description = ""
        match_description = DESCRIPTION_REGEX.search(doc_string)
        if match_description:
            description = strip_rows(match_description.group("description_method"))
        parsed_doc_string = ParsedDocString(
            description=description,
            example=example,
            returns=Parameter(param_type=return_type, param_description=returns),
            raises=raises,
            args=parameters,
            yields=Parameter(param_type=yield_type, param_description=yields),
            attributes=attributes,
            note=notes,
            to_do=to_dos,
        )
        return parsed_doc_string
