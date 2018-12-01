# coding: utf-8
"""
Python Virtualenv tools.

Gives useful information about the current virtualenv.
Such as : files locations if stakkr is installed as a package or directly cloned
"""

from os import getcwd, listdir
from os.path import dirname, realpath


def get_lib_basedir():
    """Return the base directory of stakkr, where all files are, to read services and config."""
    return dirname(realpath(__file__))


def get_dir(directory: str):
    """Detect if stakkr is a package or a clone and gives the right path for a directory."""
    return '{}/{}'.format(get_lib_basedir(), directory)


def get_file(directory: str, filename: str):
    """Detect if stakkr is a package or a clone and gives the right path for a file."""
    return get_dir(directory) + '/' + filename.lstrip('/')


def find_project_dir():
    path = getcwd()
    while True:
        files = listdir(path)
        if 'stakkr.yml' in files:
            return path

        new_path = dirname(path)
        if new_path == path:
            raise FileNotFoundError('Could not find config file (stakkr.yml)')
        path = new_path
