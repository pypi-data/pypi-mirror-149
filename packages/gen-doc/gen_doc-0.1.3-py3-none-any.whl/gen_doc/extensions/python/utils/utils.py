"""
utils for parsing module
"""


def strip_rows(doc_string: str) -> str:
    """
    Convert strings for pretty
    :param doc_string: string to process
    :type doc_string: str
    :return: converted string
    :rtype: str
    """
    lines = doc_string.expandtabs().splitlines()
    data = [line.strip() for line in lines]
    data = list(filter(lambda x: x, data))
    return "\n".join(data)
