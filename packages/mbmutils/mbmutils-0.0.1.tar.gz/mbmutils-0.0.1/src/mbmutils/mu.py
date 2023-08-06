from __future__ import annotations

import os
import re
from pathlib import Path


def get_folder_path(folder_name: str = "data") -> str | None:
    """Will search upward for first directory with a /data folder.
    includes trailing slash
    """

    def get_dir(inner_parts, num):
        return '/'.join(inner_parts[:(-1 * num)]) + '/' + folder_name

    cwd = os.getcwd()
    parts = cwd.split('/')
    for idx in range(0, len(parts) - 1):
        dir_test = get_dir(parts, idx)
        exists = os.path.isdir(dir_test)
        if exists:
            return dir_test + '/'  # include trailing slash

    return None


def get_full_path(partial_path: str = None) -> str | None:
    """
    Looking for a full path to a file that you have a partial
    or relative path for? This function will search upwards
    using the partial path provided looking for something that
    matches and will return the full path.

    :param partial_path: String
    :return: String | None
    """
    if partial_path is None:
        return None

    # remove leading slash
    partial_path = partial_path.lstrip('/')

    def _get_new_path(inner_parts, num):
        return '/'.join(inner_parts[:(-1 * num)]) + '/' + partial_path

    def _has_trail_slash(path):
        res = re.search('/$', path)
        return res is not None

    def _add_trail_slash_if_required(path):
        # not a directory
        if Path(path).is_dir() == False:
            return path
        if _has_trail_slash(path):
            return path

        return path + "/"

    cwd = os.getcwd()
    parts = cwd.split('/')
    for idx in range(0, len(parts) - 1):
        new_path = _get_new_path(parts, idx)
        if Path(new_path).exists():  # works for both file and folders
            return _add_trail_slash_if_required(new_path)

    return None


def f_between(string: str, look_for_left: str, look_for_right: str) -> str | None:
    """ Returns string found between the tokens.

    - Both tokens are required in the string, otherwise `None` is returned.
    """
    if string is None or len(string) < 1: return None
    if look_for_left is None or len(look_for_left) < 1: return None
    if look_for_right is None or len(look_for_right) < 1: return None
    if look_for_left not in string: return None
    if look_for_right not in string: return None


def f_left(string: str, look_for: str) -> str | None:
    if string is None or len(string) < 1: return None
    if look_for is None or len(look_for) < 1: return None
    if look_for not in string: return None

    return string.split(look_for)[0]


def f_left_back(string: str, look_for: str) -> str | None:
    if string is None or len(string) < 1: return None
    if look_for is None or len(look_for) < 1: return None
    if look_for not in string: return None

    return look_for.join(string.split(look_for)[:-1])


def f_replace_for(string: str, look_for: str, replace_with: str) -> str:
    """ Replaces one string with another"""
    return string.replace(look_for, replace_with)


def f_right(string: str, look_for: str) -> str | None:
    if string is None or len(string) < 1: return None
    if look_for is None or len(look_for) < 1: return None
    if look_for not in string: return None

    return look_for.join(string.split(look_for)[1:])


def f_right_back(string: str, look_for: str) -> str | None:
    if string is None or len(string) < 1: return None
    if look_for is None or len(look_for) < 1: return None
    if look_for not in string: return None

    return string.split(look_for)[-1]


def list_index_of(arr, find_val) -> int:
    if "list" not in str(type(arr)):
        raise Exception("Not a list: " + str(type(arr)))
    try:
        return arr.index(find_val)
    except:
        return -1


if __name__ == '__main__':
    print(f"Hello {f_right_back('Hello there crazy World', ' ')}!")
