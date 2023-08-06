"""Utils for handling IO and JSON operations."""
import json
from os import path, makedirs

from typing import Union, TextIO


def abs_filename(file: str) -> str:
    """
    Return the absolute filepath of a file
    :param file:
    :return:
    """
    return path.abspath(file)


def prepare(file: str, default: str = "{}"):
    """
    Prepare a file (check if it exists and create it if not)
    :param file: File to open
    :param default: default to save if file is nonexistent
    :return: A TextIO representing the file
    """
    if not path.exists(file):
        makedirs(path.dirname(file), exist_ok=True)
        with open(file, "w+") as writeable:
            writeable.write(default)
            writeable.close()


class JSONFile:
    """A JSON file on the disk"""

    __filename: str
    json: Union[dict, list]
    __default: str

    def __init__(self, filename: str, default: str = "{}"):
        """
        Create a new json file instance and load data from disk
        :param filename: filename
        :param default: default data to save if file is empty / nonexistent
        """
        self.__filename = filename
        self.__default = default
        self.reload()

    def reload(self):
        """
        Reload from disk
        :return:
        """
        prepare(self.__filename, default=self.__default)
        with open(self.__filename, "r") as file:
            self.json = json.load(file)

    def save(self):
        """
        Save the data to the disk
        :return:
        """
        prepare(self.__filename, default=self.__default)
        with open(self.__filename, "w") as file:
            json.dump(self.json, file, indent=4, sort_keys=True)
