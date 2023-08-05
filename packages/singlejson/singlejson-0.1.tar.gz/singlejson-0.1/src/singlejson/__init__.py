"""
A package for easily maintaining JSON files

open a JSON file using open()
if you call open with the same filename again, the same object will be returned.
sync all changes to disk using sync()
"""
from typing import List as _List

from utils import abs_filename as _abs_filename
from utils import JSONFile

VERSION: str = "0.1"  # Current version
_file_pool: _List[JSONFile] = {}


def load(filename: str, default: str = "{}") -> JSONFile:
    """
    Open a JsonFile (synchronously)
    :param filename: Path to JSON file on disk
    :param default: Default file contents to save if file is nonexistent
    :return: the corresponding JsonFile
    """
    filename = _abs_filename(filename)
    if filename not in _file_pool:
        _file_pool[filename] = JSONFile(filename, default=default)
    return _file_pool[filename]


def sync():
    """
    Sync changes to the filesystem
    :return:
    """
    for file in _file_pool:
        file.save()
