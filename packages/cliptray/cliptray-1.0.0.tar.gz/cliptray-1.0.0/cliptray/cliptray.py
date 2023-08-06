#!/usr/bin/env python3
"""
A Tray icon tool allowing to quickly copy some values to the clipboard.
Usage:
cliptray
"""
import os
import pyperclip
import pystray
import json
from pathlib import Path

from . import icon as clipicon


def _generate_lambda(password):
    """
    Returns a lambda for copying a code for a given key.
    :param key: The key for which the lambda should be generated.
    :returns: Lambda for copying a code for a given key.
    """
    return lambda: pyperclip.copy(password)


def _create_menu(keys):
    """
    Creates a list of menu items for each passed key.
    :param keys: A list of lists with 2 items each. The first item is a label, the second an item to copy.
    :returns: A list of menu items for each passed key.
    """
    assert all(len(key) == 2 for key in keys)
    menu = [pystray.MenuItem(key[0], _generate_lambda(key[1])) for key in keys]

    menu.append(pystray.Menu.SEPARATOR)
    menu.append(pystray.MenuItem("Exit", lambda icon: icon.stop()))
    return menu


def main():
    """
    Creates a tray icon with a menu that allows to copy items to the clipboard.
    """
    jsonFile = open(os.path.join(Path.home(), "clipboard.json"))
    icon = pystray.Icon('passtray', icon=clipicon.create_icon(),
                        menu=_create_menu(json.load(jsonFile).items()))
    icon.run()


if __name__ == '__main__':
    main()