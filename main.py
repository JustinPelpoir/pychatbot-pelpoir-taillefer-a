from functions import *

fichiers = liste_fichiers("speeches", ".txt")

conversion_minuscule(fichiers)

retrait_ponctuation(fichiers)


print(mots_importants("cleaned/"))
