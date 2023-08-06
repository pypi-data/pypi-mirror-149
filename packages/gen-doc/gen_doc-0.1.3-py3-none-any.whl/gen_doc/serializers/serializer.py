"""
 Module with base class for the serializers
"""
import os
from abc import ABC, abstractmethod
from distutils.util import strtobool
from logging import Logger, getLogger
from pathlib import Path
from typing import List, Optional, Union

from gen_doc.models import GeneralInfo, Module
from gen_doc.settings import DEFAULT_SUFFIX, NAME_FILE_GENERAL_INFO


class GenDocSerializer(ABC):
    """
    Base class for the serializers
    """

    def __init__(
        self,
        path_to_save: Optional[Path],
        root_folder: Optional[Path],
        logger: Optional[Logger] = None,
        language: Optional[str] = "python",
        extract_with_same_hierarchy: Optional[bool] = True,
        overwrite_if_file_exists: Optional[bool] = False,
        file_to_save: Optional[Union[str, Path]] = None,
        general_info: Optional[GeneralInfo] = None,
    ):
        self._logger = logger or getLogger(__name__)
        self._language = language
        self._extract_with_same_hierarchy = strtobool(str(extract_with_same_hierarchy))
        self._overwrite_if_file_exists = strtobool(str(overwrite_if_file_exists))
        self._general_info = general_info
        self._path_to_save = path_to_save
        self._root_folder = root_folder
        self._path_to_save.mkdir(exist_ok=True, parents=True)
        if not file_to_save:
            self._file_to_save = Path(
                self._path_to_save.absolute().name + DEFAULT_SUFFIX + self.suffix_file
            )
        else:
            self._file_to_save = Path(file_to_save)
            if self._file_to_save.suffix != self.suffix_file:
                self._file_to_save = Path(self._file_to_save.name + self.suffix_file)

    @property
    def suffix_file(self) -> str:
        """File type for which this serializer is intended
        :return: ".type"
        :rtype: str
        """
        raise NotImplementedError

    @property
    def short_name(self) -> str:
        """Property for short name in commands
        :return: str short name
        :rtype: str
        :example:
        >>> short_name = "md"
        """
        raise NotImplementedError

    @abstractmethod
    def serialize_module(self, module: Module, *args, **kwargs) -> List[str]:
        """Main method for serialize module
        method to implement in child classes
        :param module: object of module
        :type module: Module
        :param args: Optional arguments
        :param kwargs: Optional keyword arguments
        :return: serialized module to list of string
        :rtype: List[str]
        """
        raise NotImplementedError

    @abstractmethod
    def serialize_general_info(self) -> List[str]:
        """Method serialize general info
        :return:
        """
        raise NotImplementedError

    def serialize(self, modules: List[Module]) -> None:
        """Serialize parsed modules
        :param modules: list parsed modules
        :type modules: List[Module]
        :return: nothing
        """
        serialized_general = self.serialize_general_info()
        if self._extract_with_same_hierarchy:
            try:
                name_file = Path(NAME_FILE_GENERAL_INFO + self.suffix_file)
                self._save_documentation_file(
                    self._path_to_save / name_file, serialized_general
                )
            except Exception as exc:
                self._logger.warning(
                    "Don't save general info. Error: %s", str(exc), exc_info=True
                )
            for module in modules:
                relative_path_to_module = str(module.path_to_file.absolute())[
                    len(str(self._root_folder.absolute())) :
                ]
                val = self._path_to_save
                tmp_path = Path(str(val) + relative_path_to_module)
                path_to_tmp_root = tmp_path.parent
                path_to_tmp_root.mkdir(exist_ok=True, parents=True)
                path_to_save = path_to_tmp_root / Path(
                    module.path_to_file.stem + self.suffix_file
                )
                self._save_documentation_file(
                    path_to_save, self.serialize_module(module)
                )
        else:
            one_documentation = [
                row for module in modules for row in self.serialize_module(module)
            ]
            serialized_general.extend(one_documentation)
            self._save_documentation_file(
                self._path_to_save / self._file_to_save, serialized_general
            )

    def _save_documentation_file(
        self, path_to_save: Path, data_to_save: List[str]
    ) -> None:
        """Method to save data to a file
        :param Path path_to_save: path to file
        :type path_to_save: Path
        :param List[str] data_to_save: data to save
        :type data_to_save: List[str]
        :return: nothing
        """

        if not data_to_save:
            self._logger.warning("Not data to save for file: %s.", str(path_to_save))
            return
        if os.path.isfile(path_to_save):
            if not self._overwrite_if_file_exists:
                self._logger.warning(
                    "File with same name was exist. "
                    "Path to save: %s. "
                    "Change path to save or option "
                    "`overwrite_if_file_exists` set as True",
                    path_to_save,
                )
                return
        path_to_save.parent.mkdir(exist_ok=True, parents=True)
        with open(path_to_save, "w", encoding="utf-8") as file:
            file.write(f"{os.linesep}".join(data_to_save))
