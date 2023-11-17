from functions import *

fichiers = liste_fichiers("speeches", ".txt")

conversion_minuscule(fichiers)

retrait_ponctuation(fichiers)


# print(Inverse_Document_Frequency("cleaned/", fichiers))

# print(term_frequency()