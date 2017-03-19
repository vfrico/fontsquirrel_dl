#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This script is used as main program."""
import sys
import getopt
from fontsquirrel import FontSquirrel
from fuzzywuzzy import fuzz


def install_font(font_name):
    """Will download and install the selected font."""
    print("Install", font_name)
    fs = FontSquirrel()


    matches = search_match(families, font_name)



    for family in all_families:
        if family[0] == match:
            fs.get_family(family[1], "~/.fonts/font_downloader/")

def find_font(font_name):
    """Will download and install the selected font."""
    print("find")
    if len(matches) == 1 and False:
        match = matches[0][0]
    else:
        print("\nSe han encontrado {0} fuentes que coinciden con tu búsqueda:".format(len(matches)))
        for opt in range(0, len(matches)):
            print('\t{0}:   {1}\t{2}'.format(opt + 1, matches[opt][0], matches[opt][1]))

        option = int(input("Seleccione la opcion: ")) - 1
        print ("Descargando la fuente \""+matches[option][0]+"\" a ~/.fonts/ ")
        match = matches[option][0]


class FontDl:
    def __init__(self):
        self.fs = FontSquirrel()
        # All families from fontsquirrel_downloader
        self.all_font_info = self.fs.get_font_list(force_download=False)

    def main(self, argument):
        """The main function, which will start the program."""
        print("entrada", argument)

        if argument[0] == "install":
            try:
                self.install_font(argument[1])
            except IndexError as e:
                print("You should specify a font name")
        if argument[0] == "find":
            self.find_font(argument[1])

    def install_font(self, font_name):
        print('install')
        # All families listed on a simpler way
        families_pair = [(family['family'], family['family_url'])
                         for family in self.all_font_info]
        families = [family['family'] for family in self.all_font_info]

        # Catch the first match
        selected_font = self.search_match(families, font_name)[0]

        pair = [pair for pair in families_pair if pair[0] == selected_font][0]

        print("Installing {} family.".format(pair[0]))
        self.fs.get_family(pair[1], "~/.fonts/font_downloader/")




    def search_match(self, all_fonts, requested_font, min_score=65):
        matches = []
        for font_name in all_fonts:
            score = fuzz.token_set_ratio(font_name, requested_font)
            score += fuzz.partial_ratio(font_name, requested_font)
            score += fuzz.ratio(font_name, requested_font)
            score = int(score / 3)
            if score > min_score:
                matches.append((font_name, score))

        return sorted(matches, key=lambda score: score[1], reverse=True)


if __name__ == "__main__":
    # main(sys.argv[1:])
    m = FontDl()
    m.main(sys.argv[1:])
