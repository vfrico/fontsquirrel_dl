#a = FontSquirrel()
# a.get_font_list()
#a.get_family("roboto", "font/")
#a.get_all_families("")

from fontsquirrel import FontSquirrel
from fuzzywuzzy import fuzz
all_families = FontSquirrel().get_font_list(force_download=False)
fuente = input("Busca esta fuente: ")

found = []
for i in all_families:
    name = i['family']

    if fuzz.partial_ratio(fuente, name) > 70:
        found.append(i['family_url'])

#print(found)



#else:
#    print("La fuente "+fuente+" no ha podido ser encontrada")
print("\nSe han encontrado {0} fuentes que coinciden con tu búsqueda:".format(len(found)))
for opt in range(0,len(found)):
    print('\t{0}:   {1}'.format(opt+1,found[opt]))

option = input("Seleccione la opcion")
print ("Descargando la fuente \""+found[option]+"\" a ~/.fonts/ ")
FontSquirrel().get_family(found[option],"/home/victor/.fonts/pruebas/")
