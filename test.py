#a = FontSquirrel()
# a.get_font_list()
#a.get_family("roboto", "font/")
#a.get_all_families("")

from fontsquirrel import FontSquirrel
a = FontSquirrel().get_font_list(force_download=True)
fuente = input("Busca esta fuente: ")

found = False
for i in a:
    name = i['family']
    if name.lower() == fuente.lower():
        found = True
        fuente = i['family_url']
        print("Estás buscando la fuente: "+name)
        print (i)
        break
        
if found:
    print ("Descargando la fuente \""+fuente+"\" a ~/.fonts/ ")
    FontSquirrel().get_family(fuente,"/home/vfrico/.fonts/pruebas/")
else:
    print("La fuente "+fuente+" no ha podido ser encontrada")
