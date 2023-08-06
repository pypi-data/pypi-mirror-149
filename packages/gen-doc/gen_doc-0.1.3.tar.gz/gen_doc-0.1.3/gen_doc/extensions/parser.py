"""
Module with base file parser
"""
import os
from abc import ABC, abstractmethod
from collections import Iterable
from logging import Logger, getLogger
from pathlib import Path
from typing import List, Optional, Tuple, Union

from gen_doc.models import Module


class GenDocParser(ABC):
    """
    Base class for parsers
    """

    def __init__(
        self,
        logger: Optional[Logger] = None,
        path_to_root_folder: Optional[Union[Path, str]] = None,
        additional_files_to_ignore: Optional[List[str]] = None,
        additional_folders_to_ignore: Optional[List[str]] = None,
    ):
        self._logger = logger or getLogger(__name__)
        if not path_to_root_folder:
            path_to_root_folder = "./"
        if isinstance(path_to_root_folder, str):
            path_to_root_folder = Path(path_to_root_folder)

        self._root_folder = path_to_root_folder

        if not additional_files_to_ignore or not isinstance(
            additional_files_to_ignore, Iterable
        ):
            additional_files_to_ignore = list()  # type: List[str] # type: ignore # noqa
        if not additional_folders_to_ignore or not isinstance(
            additional_folders_to_ignore, Iterable
        ):
            additional_folders_to_ignore = (
                list()
            )  # type: List[str] # type: ignore # noqa

        self._additional_folders_to_ignore = additional_folders_to_ignore
        self._additional_files_to_ignore = additional_files_to_ignore

    @property
    def language(self) -> str:
        """Property for which language
        :return: str language
        :rtype: str
        :example:
        >>> language = "python"
        """
        raise NotImplementedError

    @property
    def short_name(self) -> str:
        """Property for short name in commands
        :return: str short name
        :rtype: str
        :example:
        >>> short_name = "py"  # for python
        """
        raise NotImplementedError

    @property
    def types_of_file_to_process(self) -> List[str]:
        """Property for concrete language
        type of documents for which to create documentation
        :return: is list of string types to build docs
        :rtype: List[str]
        :example:
        >>> types_of_file_to_process = ['.py']  # for python
        """
        raise NotImplementedError

    @property
    def files_to_ignore(self):
        """Which files names will not be considered
        :return: list of files that should not be processed
        :rtype: List[str]
        :example:
        >>> files_to_ignore = ['setup.py'] # for python
        """
        raise NotImplementedError

    @property
    def folders_to_ignore(self):
        """Which folder names will not be considered
        :return: list of folders that should not be processed
        :rtype: List[str]
        :example:
        >>> folders_to_ignore = ['__pycache__'] # for python
        """
        raise NotImplementedError

    @abstractmethod
    def parse_file(self, path_to_file: Path):
        raise NotImplementedError

    def parse(self) -> List[Module]:
        """Method parses all nested files and folders if
         they are not in the exclusion
        :return: list of parsed modules
        """
        self._logger.debug("Started process root folder: %s", self._root_folder)
        list_parsed_modules = list()  # type: List[Module]
        list_folders_with_files_to_parse = [
            (Path(dir_path), file_names)
            for (dir_path, dir_names, file_names) in os.walk(self._root_folder)
            if file_names
        ]  # type: List[Tuple[Path, List[str]]]
        _current_files_to_ignore = [
            *self.files_to_ignore,
            *self._additional_files_to_ignore,
        ]
        _current_folders_to_ignore = [
            *self.folders_to_ignore,
            *self._additional_folders_to_ignore,
        ]
        for folder_path, list_files in list_folders_with_files_to_parse:
            if not self._is_correct_folder_to_process(
                str(folder_path), _current_folders_to_ignore
            ):
                self._logger.debug("Ignore folder %s", folder_path)
                continue
            self._logger.info("Started process folder %s", folder_path)
            for file in list_files:
                if file in _current_files_to_ignore:
                    self._logger.debug(
                        "Ignore file: %s, from folder %s", file, folder_path
                    )
                    continue
                file_path = Path(file)
                if file_path.suffix not in self.types_of_file_to_process:
                    continue
                list_parsed_modules.append(
                    self.parse_file(path_to_file=folder_path / file_path)
                )

            self._logger.info("Finished process folder %s", folder_path)
        self._logger.debug("Finished process root folder: %s", self._root_folder)
        return list_parsed_modules

    @staticmethod
    def _is_correct_folder_to_process(
        folder: str, folders_to_ignore: List[str]
    ) -> bool:
        """Method to check if the specified directory
         should be processed
        :param folder: current folder to process
        :type folder: str
        :param folders_to_ignore: folders in exclusion
        :type folders_to_ignore: List[str]
        :return: true if folder needs to be processed
        :rtype: bool
        """
        for ig_folder in folders_to_ignore:
            if ig_folder == folder[-len(ig_folder) :]:
                return False
        return True
