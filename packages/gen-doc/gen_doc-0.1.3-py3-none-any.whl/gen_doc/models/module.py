"""
Models for module
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from .variables import EnumTypeVariables


class EntityOfCode(BaseModel):
    pass


class Entity(EntityOfCode):
    e_type: EnumTypeVariables = Field(None, description="Type of entity")
    e_value: List[Union[Entity, Any]] = Field(None, description="Value of entity")


class Module(BaseModel):
    path_to_file: Path = Field(description="Path to file from root folder")
    module_doc_string: Optional[str] = Field(None, description="Doc string for module")
    list_entities: List[EntityOfCode] = Field(None, description="Parsed entities")


class Argument(EntityOfCode):
    arg: str = Field(description="Title argument")
    annotation: Entity = Field(None, description="Parsed annotation to argument")
    type_comment: Any = Field(None, description="Optional info about the argument")


class Arguments(EntityOfCode):
    args: List[Argument] = Field(None, description="Parsed arguments")
    defaults: List[Entity] = Field(
        None, description="Parsed default values of arguments"
    )
    kw_defaults: List[Entity] = Field(
        None, description="Parsed default values of kwarguments"
    )
    kwarg: Optional[Argument] = Field(None, description="Parsed **kwarg")  # **kwarg
    vararg: Optional[Argument] = Field(None, description="Parsed *args")  # *args
    posonlyargs: List[Argument] = Field(
        None, description="Parsed position-only arguments"
    )
    kwonlyargs: List[Argument] = Field(
        None, description="Parsed keyword-only arguments"
    )


class Parameter(BaseModel):
    param_name: str = Field(None, description="Parsed parameter name")
    param_type: str = Field(None, description="Parsed parameter type")
    param_description: str = Field(None, description="Parsed parameter description")


class ParsedDocString(BaseModel):
    description: str = Field(None, description="Parsed function description")
    args: List[Parameter] = Field(None, description="Parsed arguments")
    raises: List[Parameter] = Field(None, description="Parsed raises of function")
    returns: Parameter = Field(None, description="Parsed return values of function")
    yields: Parameter = Field(None, description="Parsed yield values of function")
    note: str = Field(None, description="Parsed note")
    example: str = Field(None, description="Parsed example")
    extra_params: Optional[Dict[str, str]] = Field(None, description="Parsed extra")
    to_do: Optional[List[str]] = Field(None, description="Parsed arguments")
    attributes: Optional[List[Parameter]] = Field(None, description="Parsed arguments")

    def _get_numerical_equivalent_of_parsing(self) -> int:
        _sum = 0
        properties = self.schema()["properties"]
        for property in properties:
            if self.__getattribute__(property):
                _sum += 1
        return _sum

    def __lt__(self, other):
        if not other:
            return False
        return (
            self._get_numerical_equivalent_of_parsing()
            < other._get_numerical_equivalent_of_parsing()
        )


class Function(EntityOfCode):
    function_name: str = Field(None, description="Function name")
    function_doc_string: str = Field(None, description="Function doc string")
    function_args: Arguments = Field(None, description="Function arguments")
    function_decorators: List[Entity] = Field(None, description="Function decorators")
    function_returns: Entity = Field(None, description="What does the function return")
    function_type_comment: Any = Field(None, description="Function type comment")
    function_is_async: bool = Field(False, description="Is async function")
    function_entities: List[EntityOfCode] = Field(
        None, description="Sub entities current function"
    )
    function_parsed_docstring: Optional[ParsedDocString] = Field(
        None, description="Docstring object resolved to object"
    )


class Assign(EntityOfCode):
    name: Entity = Field(None, description="Name variable")
    value: Entity = Field(None, description="Value variable")
    annotation: Entity = Field(None, description="Type annotation variable")
    type_comment: Any = Field(None, description="Optional argument")
    simple: Any = Field(None, description="Optional argument")


class Class(EntityOfCode):
    class_name: str = Field(None, description="Class name")
    class_doc_string: str = Field(None, description="Class doc string")
    class_decorators: List[Entity] = Field(None, description="Class decorators")
    class_bases: List[Entity] = Field(None, description="Class bases")
    class_keywords: List[Assign] = Field(None, description="Class keywords")
    class_entities: List[EntityOfCode] = Field(
        None, description="Sub entities current class"
    )
    class_parsed_docstring: Optional[ParsedDocString] = Field(
        None, description="Docstring object resolved to object"
    )
