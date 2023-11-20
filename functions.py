import os
import math


# Extraire les noms des fichiers texte
def liste_fichiers(repertoire, extension):

    noms_fichier = []
    for filename in os.listdir(repertoire):
        if filename.endswith(extension):
            noms_fichier.append(filename)
    return noms_fichier


# Extraction et affichage des noms des présidents à partir de la liste des noms des fichiers texte
def extraction_nom(liste_nom_fichier):
    liste_noms_presidents = set()

    for i in range(0, len(liste_nom_fichier)):
        # Retirer l'extension .txt
        nom_president = os.path.splitext(liste_nom_fichier[i])[0]

        # Retirer les informations annexes
        nom_president = nom_president.split("_")
        nom_president = nom_president[1]
        nom_president = nom_president.split("1")
        nom_president = nom_president[0]
        nom_president = nom_president.split("2")
        nom_president = nom_president[0]

        # AJouter le nom du président à la liste des présidents
        liste_noms_presidents.add(nom_president)

    return liste_noms_presidents


# Convertir les textes des fichiers en minuscule
def conversion_minuscule(liste_noms_fichier):
    for i in range(0, len(liste_noms_fichier)):
        with (open("speeches/"+liste_noms_fichier[i], "r") as fichier_original,
              open("cleaned/"+liste_noms_fichier[i], "w") as fichier_clean
              ):

            for ligne in fichier_original:
                for caractere in ligne:
                    if ord(caractere) >= 65 and ord(caractere) <= 90:
                        fichier_clean.write(chr(ord(caractere) + 32))
                    else:
                        fichier_clean.write(caractere)


# Retrait des ponctuations dans les textes nettoyés
def retrait_ponctuation(liste_noms_fichier):

    # Lecture de chaque fichier texte
    for i in range(0, len(liste_noms_fichier)):
        with open("cleaned/"+liste_noms_fichier[i], "r") as fichier:
            texte = fichier.read()

        # Modification un par un des fichiers texte
        with open("cleaned/"+liste_noms_fichier[i], "w") as fichier:
            for ligne in texte:
                for caractere in ligne:

                    # Code ASCII des ponctuations
                    liste_ponctuation_retrait = [33, 34, 44,
                                                 46, 58, 59, 63,
                                                 96, 130, 132,
                                                 133, 145, 146,
                                                 147, 148, 149,
                                                 ]
                    # Code ASCII de "-" et l'apostrophe
                    liste_ponctuation_speciale = [39, 45]

                    # Remplacer les ponctuations par un blanc
                    if ord(caractere) in liste_ponctuation_retrait:
                        fichier.write("")

                    # Remplacer "-" et apostrophes par un espace
                    elif ord(caractere) in liste_ponctuation_speciale:
                        fichier.write(" ")
                    else:
                        fichier.write(caractere)


# Associer à chaque nom le prenom
def prenoms(liste_noms_presidents):
    dico_prenom = {"Chirac": "Jacques",
                   "Macron": "Emmanuel",
                   "Mitterand": "Francois",
                   "Hollande": "Francois",
                   "Giscard dEstaing": "Valery",
                   "Sarkozy": "Nicolas"
                   }
    for i in range(len(liste_noms_presidents)):
        prenom = dico_prenom[liste_noms_presidents[i]]
        liste_noms_presidents[i] = liste_noms_presidents[i] + prenom
    return liste_noms_presidents


# fonction pour déterminer un dictionaire avec chaque mot associés à leur occurrence
def term_frequency(chaine):
    # Diviser la chaine de caractère en une liste de mots
    mots = chaine.split()
    dico_TF = {}     # dictionnaire
    mots_check = []

    for i in range(0, len(mots)):

        # Vérifier si un mot n'a pas déjà été analysé
        if mots[i] not in mots_check:
            occurrence = 0

            # Occurrence du mot dans la phrase
            for j in range(0, len(mots)):
                if mots[i] == mots[j]:
                    occurrence += 1
            # Ajout du mot
            mots_check.append(mots[i])

            # Association de chaque mot à son nombre d'occurrences
            dico_TF[mots[i]] = occurrence

    return dico_TF


def Inverse_Document_Frequency(repertoire):
    dico_IDF = {}
    fichiers = liste_fichiers(repertoire, ".txt")

    # Pour chaque fichier texte, vérification de la présence des mots
    for i in range(0, len(fichiers)):

        # Lecture du fichier texte
        with open(repertoire+fichiers[i], "r") as fichier:
            texte = fichier.read()

        mots = texte.split()
        mots_check = []

        for i in range(0, len(mots)):
            # Vérifier si un mot n'a pas déjà été analysé dans le même fichier texte
            if mots[i] not in mots_check:
                # Vérifier si le mot est déjà dans un autre fichier
                if mots[i] in dico_IDF.keys():
                    dico_IDF[mots[i]] += 1
                else:
                    dico_IDF[mots[i]] = 1

                # Ajout du mot dans la liste des mots analysés
                mots_check.append(mots[i])

    # Pour chaque mot dans les textes, calcul du poids du mot
    for cle in dico_IDF.keys():
        dico_IDF[cle] = math.log10(len(fichiers) / (dico_IDF[cle]))

    return dico_IDF


def score_tf_idf(repertoire):
    dico_tf_idf = {}
    fichiers = liste_fichiers(repertoire, ".txt")

    # Appeler la valeur IDF de chacun des mots dans les textes du répertoire
    idf = Inverse_Document_Frequency(repertoire)

    # Création d'une liste pour chaque mot stockant le score TF-IDF pour chaque document
    for cle in idf.keys():
        dico_tf_idf[cle] = []

    for i in range(0, len(fichiers)):

        # Ouverture de chaque texte un par un
        with open(repertoire+fichiers[i], "r") as fichier:
            texte = fichier.read()
            tf = term_frequency(texte)      # Appel de la valeur TF des mots du texte analysé

            # Ajout du score TF-IDF de chaque mot
            for cle_idf in idf.keys():
                if cle_idf not in tf.keys():
                    dico_tf_idf[cle_idf].append(0)

                elif cle_idf in tf.keys():
                    dico_tf_idf[cle_idf].append(idf[cle_idf] * tf[cle_idf])

    return dico_tf_idf
