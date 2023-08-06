import pathlib
import re
from typing import Optional


def get_version() -> Optional[str]:
    """
      Method for getting the version of the library from the init file
    :requirements: version must be specified separately
        :good: __version__ = '0.0.1'
        :bad: __version__, __any_variable__ = '0.0.1', 'any_value'
    :return: version lib
    """
    root_lib = pathlib.Path(__file__).parent.parent
    txt = (root_lib / "__init__.py").read_text("utf-8")
    txt = txt.replace("'", '"')
    try:
        version = re.findall(r'^__version__ = "([^"]+)"\r?$', txt, re.M)[0]
        return version
    except IndexError:
        raise RuntimeError("Unable to determine version.")
