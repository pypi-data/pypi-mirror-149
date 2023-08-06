"""
Module with functions work with  config
"""
import logging
from pathlib import Path
from shutil import copyfile
from typing import Any, Dict, Optional

import yaml  # type: ignore  # noqa


def normalize_name_config(file_name_to_save: str) -> Path:
    """Help function to normalize and rename the file
    :param str file_name_to_save: name file
    :type file_name_to_save: str
    :return: path to file
    :rtype: Path
    """
    path_to_save = Path(file_name_to_save)
    if path_to_save.suffix != ".yaml":
        path_to_save = Path(path_to_save.name + ".yaml")
    return path_to_save


def load_config(file_name_to_save: str) -> Optional[Dict[str, Any]]:
    """Method to parse the config file
    :param file_name_to_save: path to file config
    :type file_name_to_save: str
    :return: config if exists
    :rtype: Optional[Dict[str, Any]]
    """
    path_to_config_file = normalize_name_config(file_name_to_save)
    if not path_to_config_file.is_file():
        return None
    try:
        with open(normalize_name_config(file_name_to_save), "r") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as exc:
        logging.warning("Error in time load config. Error: %s", str(exc), exc_info=True)
    return dict()


def copy_config(file_name_to_save: str, overwrite: bool) -> bool:
    """Method to copy config template
    :param file_name_to_save: name config
    :type file_name_to_save: str
    :param overwrite: is overwriting config if exist
    :type overwrite: bool
    :return: is correct
    :rtype: bool
    """
    config_path = (
        Path(__file__).absolute().parent.parent / Path("src") / Path("template.yaml")
    )
    path_to_config_file = normalize_name_config(file_name_to_save)
    if path_to_config_file.is_file():
        if not overwrite:
            print("Such file already exists. To replace use the command '-o'")
            return False
    copyfile(config_path, path_to_config_file)
    return True
