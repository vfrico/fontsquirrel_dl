#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This script is used as main program."""
import sys
import getopt
from fontsquirrel import FontSquirrel
from fuzzywuzzy import fuzz


def main(argument):
    """The main function, which will start the program."""
    print(argument)

    if argument[0] == "install":
        try:
            install_font(argument[1])
        except IndexError as e:
            print("You should specify a font name")
    if argument[0] == "find":
        find_font(argument[1])


def install_font(font_name):
    """Will download and install the selected font."""
    print("Install", font_name)
    fs = FontSquirrel()
    # All families from fontsquirrel_downloader
    families = fs.get_font_list(force_download=False)
    all_families = [(family['family'], family['family_url']) for family in families]
    families = [family['family'] for family in families]

    matches = []
    for name in families:
        score = fuzz.partial_ratio(font_name, name)
        if score > 70:
            matches.append((name, score))

    # matches = process.extractBests(font_name, families)
    matches = sorted(matches, key=lambda score: score[1], reverse=True)
    if len(matches) == 1:
        match = matches[0][0]
    else:
        print("\nSe han encontrado {0} fuentes que coinciden con tu búsqueda:".format(len(matches)))
        for opt in range(0, len(matches)):
            print('\t{0}:   {1}'.format(opt + 1, matches[opt][0]))

        option = int(input("Seleccione la opcion: ")) - 1
        print ("Descargando la fuente \""+matches[option][0]+"\" a ~/.fonts/ ")
        match = matches[option][0]

    for family in all_families:
        if family[0] == match:
            fs.get_family(family[1], "~/.fonts/font_downloader/")




def find_font(font_name):
    """Will download and install the selected font."""
    print("find")
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
