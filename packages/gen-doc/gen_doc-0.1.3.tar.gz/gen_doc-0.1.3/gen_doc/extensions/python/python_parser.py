"""
Module with parser for python files
Sphinx docstrings
"""
# pylint: disable=too-many-branches,too-many-return-statements,no-else-return,broad-except  # noqa
import ast
from ast import stmt
from pathlib import Path
from typing import List, Optional, Union

try:
    from ast import unparse
except ImportError:
    from astunparse import unparse  # type: ignore

from gen_doc.extensions.parser import GenDocParser

from ...models import (
    Assign,
    Class,
    Entity,
    EntityOfCode,
    EnumTypeVariables,
    Function,
    Module,
    Operations,
)
from ...models.module import Argument, Arguments
from .utils import DocStingPyParser

ARGUMENTS_TO_IGNORE = ["self"]


class GenDocPythonParser(GenDocParser):
    """
    Class to retrieve information about the python module
    """

    language = "python"
    short_name = "py"
    types_of_file_to_process = [".py"]
    folders_to_ignore = [
        "__pycache__",
        ".git",
        "venv",
        "build",
        "dist",
        ".mypy_cache",
        ".idea",
    ]
    files_to_ignore = ["setup.py"]

    def _parse_body(
        self,
        obj: Union[ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef],
        is_inner: bool = False,
    ) -> List[EntityOfCode]:
        """Method to parse object body for parse child
        :param obj: obj to process
        :type obj: Union[ast.Module, ast.ClassDef, ast.FunctionDef,
         ast.AsyncFunctionDef]
        :return: parsed body
        :rtype: List[EntityOfCode]
        """
        list_entities = list()  # type: List[EntityOfCode]
        for obj in obj.body:  # type: ignore
            parsed_obj = self._parse_obj(obj, is_inner)  # type: ignore
            if parsed_obj:
                list_entities.append(parsed_obj)
        return list_entities

    def _parse_obj(self, obj: stmt, is_inner: bool) -> Optional[EntityOfCode]:
        """Method to define the handler object
        the method contains all the objects for analysis
        :param obj: object to process if exist handler
        :type obj: stmt
        :return: type, info
        :rtype: Optional[EntityOfCode]
        """

        if isinstance(obj, (ast.Expr, ast.Import, ast.ImportFrom, ast.Assert)):
            return None
        elif isinstance(obj, (ast.Assign, ast.AnnAssign)) and not is_inner:
            return self._parse_assign(obj)
        elif isinstance(obj, ast.ClassDef):
            return self._parse_class(obj)
        elif isinstance(obj, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return self._parse_function(obj)
        else:
            self._logger.debug("Can't parse %s", obj)
        return None

    def _parse_value(self, obj: ast.expr) -> Entity:
        """Method to parse expression
        :param obj: obj to parse
        :type obj: ast.expr
        :return: parsed entity
        :rtype: Entity
        """
        if obj is None:
            return Entity(e_type=EnumTypeVariables.NONE, e_value=[None])
        elif obj in [True, False]:
            return Entity(e_type=EnumTypeVariables.BOOL, e_value=[obj])
        elif isinstance(obj, ast.Name):
            return Entity(e_type=EnumTypeVariables.NAME, e_value=[obj.id])
        elif isinstance(obj, ast.Num):
            return Entity(e_type=EnumTypeVariables.NUM, e_value=[obj.n])
        elif isinstance(obj, ast.Str):
            return Entity(e_type=EnumTypeVariables.STR, e_value=[obj.s])
        elif isinstance(obj, ast.NameConstant):
            return self._parse_value(obj.value)
        elif isinstance(obj, ast.Constant):
            return self._parse_value(obj.value)
        elif isinstance(obj, ast.Tuple):
            return Entity(
                e_type=EnumTypeVariables.TUPLE,
                e_value=[self._parse_value(val) for val in obj.elts],
            )
        elif isinstance(obj, ast.List):
            return Entity(
                e_type=EnumTypeVariables.LIST,
                e_value=[self._parse_value(val) for val in obj.elts],
            )
        elif isinstance(obj, ast.Set):
            return Entity(
                e_type=EnumTypeVariables.SET,
                e_value=[self._parse_value(val) for val in obj.elts],
            )
        elif isinstance(obj, ast.Slice):
            lower = self._parse_value(obj.lower) if obj.lower else ""
            upper = self._parse_value(obj.upper) if obj.upper else ""
            step = self._parse_value(obj.step) if obj.step else ""
            return Entity(e_type=EnumTypeVariables.SLICE, e_value=[lower, upper, step])
        elif isinstance(obj, ast.Dict):
            return Entity(
                e_type=EnumTypeVariables.DICT,
                e_value=[
                    (self._parse_value(key), self._parse_value(value))
                    for key, value in zip(obj.keys, obj.values)
                ],
            )
        elif isinstance(obj, ast.BinOp):
            return Entity(
                e_type=EnumTypeVariables.BIN_OP,
                e_value=[
                    self._parse_value(obj.right),
                    Operations[obj.op.__class__.__name__].value,
                    self._parse_value(obj.left),
                ],
            )
        elif isinstance(obj, ast.UnaryOp):
            return Entity(
                e_type=EnumTypeVariables.UNARY_OP,
                e_value=[
                    Operations[obj.op.__class__.__name__].value,
                    self._parse_value(obj.operand),
                ],
            )
        elif obj == Ellipsis:
            return Entity(e_type=EnumTypeVariables.NAME, e_value=["..."])

        else:
            self._logger.debug("Not processed: %s", obj)
            try:
                return Entity(e_type=EnumTypeVariables.UNPARSE, e_value=[unparse(obj)])
            except AttributeError:
                return Entity(
                    e_type=EnumTypeVariables.NAME, e_value=["<UnparsedObject>"]
                )

    def _parse_assign(self, obj: Union[ast.Assign, ast.AnnAssign]) -> Assign:
        """
        Parsing assigner
        :param obj: object for Parsing Assigner
        :type: Union[ast.Assign, ast.AnnAssign]
        :return: parsed all assigned
        :rtype: Assign
        """
        assign = Assign(value=self._parse_value(obj.value))
        if isinstance(obj, ast.AnnAssign):
            assign.name = self._parse_value(obj.target)
            assign.annotation = self._parse_value(obj.annotation)
            assign.simple = obj.simple
        else:
            assign.name = self._parse_value(obj.targets[0])
            assign.type_comment = obj.type_comment
        return assign

    def _parse_class(self, obj: ast.ClassDef) -> Class:
        """Method to parse a class
        :param obj: current class to parse info from
        :type obj: ast.ClassDef
        :return: processed class
        :rtype: Class
        """
        clazz = Class(class_name=obj.name, class_doc_string=ast.get_docstring(obj))
        clazz.class_decorators = self._parse_decorators(obj)
        clazz.class_bases = self._parse_basses(obj)
        clazz.class_entities = self._parse_body(obj)
        clazz.class_keywords = self._parse_keywords(obj)
        clazz.class_parsed_docstring = DocStingPyParser.parse(clazz.class_doc_string)
        return clazz

    def _parse_decorators(
        self, obj: Union[ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> List[Entity]:
        """Method to get decorators of a class or a function
        :param obj: current object to parse info from
        :type obj: Union[ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef]
        :return: list of decorators
        :rtype: List[Entity]
        """
        return [self._parse_value(decorator) for decorator in obj.decorator_list]

    def _parse_basses(self, obj: ast.ClassDef) -> List[Entity]:
        """Method to parse bases for the current class
        :param obj: current class to parse info from
        :type: ast.ClassDef
        :return: list of bases classes
        :rtype: List[Entity]
        """
        return [self._parse_value(base) for base in obj.bases]

    def _parse_keywords(self, obj: ast.ClassDef) -> List[Assign]:
        """Parse of keywords
        :param obj: current class to parse info from
        :type: ast.ClassDef
        :return: list parsed keywords
        :rtype: List[Entity]
        """
        return [
            Assign(
                name=Entity(e_type=EnumTypeVariables.NAME, e_value=[key_word.arg]),
                value=self._parse_value(key_word.value),
            )
            for key_word in obj.keywords
        ]

    def _parse_function(
        self, obj: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> Function:
        """Method to parse functions
        :param obj: current function to parse info from
        :type: Union[ast.FunctionDef, ast.AsyncFunctionDef]
        :return: parsed function object
        :rtype: Function
        """
        _function = Function(
            function_name=obj.name,
            function_doc_string=ast.get_docstring(obj),
            function_returns=self._parse_value(obj.returns),
            function_decorators=self._parse_decorators(obj),
            function_args=self._parse_arguments(obj.args),
            function_entities=self._parse_body(obj, is_inner=True),
            function_type_comment=obj.type_comment,
            function_parsed_docstring=DocStingPyParser.parse(ast.get_docstring(obj)),
        )
        if isinstance(obj, ast.AsyncFunctionDef):
            _function.function_is_async = True
        return _function

    def _parse_arguments(self, obj: ast.arguments) -> Arguments:
        """Method to parse arguments functions
        :param obj: current function to parse info from
        :return: parsed arguments of function
        :rtype: Arguments
        """
        args = [
            Argument(
                arg=arg.arg,
                annotation=self._parse_value(arg.annotation),
                type_comment=arg.type_comment,
            )
            for arg in obj.args
            if arg.arg not in ARGUMENTS_TO_IGNORE
        ]
        defaults = [self._parse_value(default) for default in obj.defaults]
        kw_defaults = [self._parse_value(default) for default in obj.kw_defaults]

        kwarg = (
            None
            if not obj.kwarg
            else Argument(
                arg=obj.kwarg.arg,
                annotation=self._parse_value(obj.kwarg.annotation),
                type_comment=obj.kwarg.type_comment,
            )
        )
        vararg = (
            None
            if not obj.vararg
            else Argument(
                arg=obj.vararg.arg,
                annotation=self._parse_value(obj.vararg.annotation),
                type_comment=obj.vararg.type_comment,
            )
        )
        kwonlyargs = [
            Argument(
                arg=arg.arg,
                annotation=self._parse_value(arg.annotation),
                type_comment=arg.type_comment,
            )
            for arg in obj.kwonlyargs
        ]
        posonlyargs = [
            Argument(
                arg=arg.arg,
                annotation=self._parse_value(arg.annotation),
                type_comment=arg.type_comment,
            )
            for arg in obj.posonlyargs
        ]
        return Arguments(
            args=args,
            kwarg=kwarg,
            defaults=defaults,
            kw_defaults=kw_defaults,
            posonlyargs=posonlyargs,
            kwonlyargs=kwonlyargs,
            vararg=vararg,
        )

    def _parse_file(self, path_to_file: Path) -> Module:
        """Main processing method
        Reads the file and starts the parsing process
        :param path_to_file: path to the file to be processed
        :type: Path
        :return: module with extracted information from the input file
        :rtype: Module
        """
        file_to_parse = open(path_to_file, "r", encoding="utf-8").read()
        tree = ast.parse(file_to_parse)
        try:
            module_doc_string = ast.get_docstring(tree)
        except Exception as exc:
            module_doc_string = ""
            self._logger.debug(
                "File `%s` don't have module doc string." " Err: %s",
                path_to_file,
                str(exc),
            )
        module = Module(path_to_file=path_to_file, module_doc_string=module_doc_string)
        module.list_entities = self._parse_body(tree)
        return module

    def parse_file(self, path_to_file: Path) -> Module:
        """Method for parsing python modules
        :param Path path_to_file: path to current file to parse info from
        :type path_to_file: Path
        :return: parsed module
        :rtype: Module
        """
        self._logger.debug("Started process file: %s", path_to_file)

        module_data = self._parse_file(path_to_file)

        self._logger.debug("Finished process file: %s", path_to_file)
        return module_data
