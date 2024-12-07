# -*- coding: utf-8 -*-

from io import open
from json import load
from string import ascii_letters, digits
import os.path

ALLOWED_CHARACTERS = set(ascii_letters)
ALLOWED_CHARACTERS.update(set(digits))
ALLOWED_CHARACTERS.update({"@", "$", "*", '"', "'"})


def get_complete_path_of_file(filename):
    """Join the path of the current directory with the input filename."""
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, filename)

# Pre-load the unicode characters
with open(get_complete_path_of_file("alphabetic_unicode.json"), "r") as json_file:
    ALLOWED_CHARACTERS.update(load(json_file))
