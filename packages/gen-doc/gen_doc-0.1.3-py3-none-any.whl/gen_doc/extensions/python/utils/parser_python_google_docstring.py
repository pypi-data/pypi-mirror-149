"""
Module with python Google docstrings parser
"""
import re
from typing import List, Optional, Tuple

from gen_doc.extensions.python.utils.utils import strip_rows
from gen_doc.models import Parameter, ParsedDocString

from .base_parser import PythonDocStringParser

GENERAL_STOPPERS = r"(?:(?=Args:)|(?=Arguments?:)|(?=Returns?:)|(?=Raises?:)|(?=Attributes?:)|(?=Examples?:)|(?=Todo?:)|(?=Notes?:)|(?=Yields?:)|(?=\.\. \_)|\Z)"  # noqa

DESCRIPTION_REGEX = re.compile(f"(?P<description>.*?){GENERAL_STOPPERS}", re.S)  # noqa

ARGS_REGEX = re.compile(
    f"(Args|Arguments?):?\s (?P<args_doc>.*?){GENERAL_STOPPERS}", re.S  # noqa
)
RETURNS_REGEX = re.compile(
    f"Returns?:?\s (?P<returns_doc>.*?){GENERAL_STOPPERS}", re.S  # noqa
)
YIELDS_REGEX = re.compile(
    f"Yields?:?\s (?P<yields_doc>.*?){GENERAL_STOPPERS}", re.S  # noqa
)

RAISES_REGEX = re.compile(
    f"Raises?:?\s (?P<raises_doc>.*?){GENERAL_STOPPERS}", re.S  # noqa
)
ATTRIBUTES_REGEX = re.compile(
    f"Attributes?:?\s (?P<attribute_doc>.*?){GENERAL_STOPPERS}", re.S  # noqa
)
EXAMPLE_REGEX = re.compile(
    f"Examples?:?\s (?P<example_doc>.*?){GENERAL_STOPPERS}", re.S  # noqa
)
NOTE_REGEX = re.compile(f"Notes?:?\s (?P<note_doc>.*?){GENERAL_STOPPERS}", re.S)  # noqa
TODO_REGEX = re.compile(f"Todos?:?\s (?P<todo_doc>.*?){GENERAL_STOPPERS}", re.S)  # noqa
OPTIONAL_ARGS_REGEX = re.compile(
    f"\.\. \_(?P<optional_name>[\*\w\s]+):?\s (?P<optional_doc>.*?){GENERAL_STOPPERS}",  # noqa
    re.S,  # noqa
)
STOPPERS_ATTR_ARG = r"(?:(?=[\r\n?|\n]{1,}[ \t\d\w\(\)\]\[\,]+:)|\Z)"  # noqa

RETURN_YIELD_PARSERS_REGEX = re.compile(
    f"(?P<type>[\s\d\w\(\)\]\[\\,]+): (?P<return_doc>.*?){STOPPERS_ATTR_ARG}",  # noqa
    re.S,  # noqa
)
STOPPERS_TODOS = r"(?:(?=\*)|\Z)"  # noqa
TODOS_PARSER_REGEX = re.compile(f"\* (?P<to_do>.*?){STOPPERS_TODOS}", re.S)  # noqa

PARAM_REGEX = re.compile(
    f"\s(?P<param>[\s\d\w\(\)\]\[\,]+): (?P<param_doc>.*?){STOPPERS_ATTR_ARG}",  # noqa
    re.S,  # noqa
)
PARSE_PARAM_TYPE = re.compile(
    f"(?P<param>[\*\w\s]+)[\s]*\((?P<type>.*?)\)", re.S  # noqa
)


class GoogleDocStringPyParser(PythonDocStringParser):
    """
    Google doc string parser
    """

    example = """
    Example google doc string

    Description of function

    Arguments:
        value1 (int): description to value1
        value2 (Dict[str, str]): description to value2
          long description
          value2 desc
        value3: description value3
    Attributes:
        value4 (int): description to value4
        value5: description to value5
    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
    Returns:
        type_returned_value: a description of return
    Todos:
        * For module TODOs
        * ToDo
          long
    .. _Google Python Style Guide optional parameters:
        http://google.github.io/styleguide/pyguide.html
    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/
    Yields:
        int: yield value with type
    Note:
        Do not include the `self` parameter in the ``Args`` section.
    Example:
        Examples should be written in doctest format, and should illustrate how
        to use the function.
        >>> print([i for i in example_generator(4)])
        [0, 1, 2, 3]
    """

    @staticmethod
    def parse(doc_string: Optional[str]) -> Optional[ParsedDocString]:
        """Function to parse doc string to a standard object
        ! google doc string style
        :param doc_string: received function doc string
        :type doc_string: str
        :return: parsed object
        :rtype:Optional[ParsedDocString]
        """

        def parse_params_type(param_type_part: str) -> Tuple[str, Optional[str]]:
            res = [
                (param.strip(), _type.strip())
                for param, _type, in PARSE_PARAM_TYPE.findall(param_type_part)
            ]
            if res:
                return res[0]
            return param_type_part.strip(), None

        def parse_attributes_args(block_doc_string: str) -> List[Parameter]:
            params = [val for val in PARAM_REGEX.findall(block_doc_string)]
            parameters = list()
            for parameter in params:
                param_type = parse_params_type(parameter[0])
                parameters.append(
                    Parameter(
                        param_name=param_type[0],
                        param_type=param_type[1],
                        param_description=strip_rows(parameter[1]),
                    )
                )
            return parameters

        def parse_return_yield_doc(parsed_doc) -> Parameter:
            params = [val for val in RETURN_YIELD_PARSERS_REGEX.findall(parsed_doc)]
            returns_parameter = Parameter()
            if not params:
                returns_parameter.param_description = strip_rows(parsed_doc)
            else:
                returns_parameter.param_type = params[0][0].strip()
                returns_parameter.param_description = strip_rows(params[0][1])
            return returns_parameter

        if not doc_string:
            return None
        parsed_doc_string = ParsedDocString()
        description = DESCRIPTION_REGEX.search(doc_string)
        if description:
            description_str = description.group("description")
            parsed_doc_string.description = strip_rows(description_str)
        arguments = ARGS_REGEX.search(doc_string)
        if arguments:
            arguments_str = arguments.group("args_doc")
            parsed_doc_string.args = parse_attributes_args(arguments_str)
        attributes = ATTRIBUTES_REGEX.search(doc_string)
        if attributes:
            attributes_str = attributes.group("attribute_doc")
            parsed_doc_string.attributes = parse_attributes_args(attributes_str)
        raises = RAISES_REGEX.search(doc_string)
        if raises:
            raises_str = raises.group("raises_doc")
            tmp_raise = parse_attributes_args(raises_str)
            for val in tmp_raise:
                val.param_type = val.param_name
            parsed_doc_string.raises = tmp_raise
        returns = RETURNS_REGEX.search(doc_string)
        if returns:
            returns_str = returns.group("returns_doc")
            parsed_doc_string.returns = parse_return_yield_doc(returns_str)
        yields = YIELDS_REGEX.search(doc_string)
        if yields:
            yields_str = yields.group("yields_doc")
            parsed_doc_string.yields = parse_return_yield_doc(yields_str)
        todos = TODO_REGEX.search(doc_string)
        if todos:
            todos_str = todos.group("todo_doc")
            params = [strip_rows(val) for val in TODOS_PARSER_REGEX.findall(todos_str)]
            parsed_doc_string.to_do = params
        optional_params = OPTIONAL_ARGS_REGEX.findall(doc_string)
        if optional_params:
            optional_params_parsed = {
                op_param[0].strip(): strip_rows(op_param[1])
                for op_param in optional_params
            }
            parsed_doc_string.extra_params = optional_params_parsed
        examples = EXAMPLE_REGEX.search(doc_string)
        if examples:
            examples_str = examples.group("example_doc")
            parsed_doc_string.example = strip_rows(examples_str)
        notes = NOTE_REGEX.search(doc_string)
        if notes:
            notes_str = notes.group("note_doc")
            parsed_doc_string.note = strip_rows(notes_str)
        return parsed_doc_string


if __name__ == "__main__":
    parser = GoogleDocStringPyParser()
    res = parser.parse(parser.example)
    print(res.returns)
