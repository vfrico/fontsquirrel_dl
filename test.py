# -*- coding: utf-8 -*-
# a = FontSquirrel()
# a.get_font_list()
# a.get_family("roboto", "font/")
# a.get_all_families("")

from fontsquirrel import FontSquirrel
from fuzzywuzzy import fuzz
# from fuzzywuzzy import process

def font_downloader(font_name=None, font_path="~/.fonts/font_downloader/"):
    # All families from fontsquirrel_downloader
    families = FontSquirrel().get_font_list(force_download=False)
    all_families = [(family['family'], family['family_url']) for family in families]
    families = [family['family'] for family in families]
    if not font_name:
        font_name = input("Introduce la fuente a buscar: ")

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
            FontSquirrel().get_family(family[1], font_path)


font_downloader()
