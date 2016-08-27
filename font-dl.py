#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This script is used as main program."""
import sys


def main(argument):
    """The main function, which will start the program."""
    if argument[0] == "install":
        install_font(argument[1])
    if argument[0] == "find":
        find_font(argument[1])


def install_font(font_name):
    """Will download and install the selected font."""
    pass


def find_font(font_name):
    """Will download and install the selected font."""
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
