# -*- coding: utf-8 -*-
#a = FontSquirrel()
# a.get_font_list()
#a.get_family("roboto", "font/")
#a.get_all_families("")

from fontsquirrel import FontSquirrel
#from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def font_downloader(font_name = None, font_path="~/.fonts/font_downloader/"):
    # All families from fontsquirrel_downloader
    all_families = FontSquirrel().get_font_list(force_download=False)
    families = [family['family'] for family in all_families]
    print (families)
    if not font_name:
        font_name = input("Introduce la fuente a buscar: ")

    matches = process.extract(font_name, families, limit=5)

    if len(matches) == 1:
        FontSquirrel().get_family(matches[0], font_path)
    else:
        print("\nSe han encontrado {0} fuentes que coinciden con tu búsqueda:".format(len(matches)))
        for opt in range(0, len(matches)):
            print('\t{0}:   {1}'.format(opt + 1, matches[opt]))

        option = input("Seleccione la opcion")
        print ("Descargando la fuente \""+matches[option]+"\" a ~/.fonts/ ")
        FontSquirrel().get_family(matches[option], font_path)


#
#
# fuente = input("Busca esta fuente: ")
#
# found = []
# for i in all_families:
#     name = i['family']
#
#     if fuzz.partial_ratio(fuente, name) > 70:
#         found.append(i['family_url'])
#
# #print(found)
#
#
#
# #else:
# #    print("La fuente "+fuente+" no ha podido ser encontrada")
# print("\nSe han encontrado {0} fuentes que coinciden con tu búsqueda:".format(len(found)))
# for opt in range(0,len(found)):
#     print('\t{0}:   {1}'.format(opt+1,found[opt]))
#
# option = input("Seleccione la opcion")
# print ("Descargando la fuente \""+found[option]+"\" a ~/.fonts/ ")
# FontSquirrel().get_family(found[option],"/home/victor/.fonts/pruebas/")
font_downloader()
