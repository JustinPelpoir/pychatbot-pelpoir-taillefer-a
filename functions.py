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
        with open(repertoire+fichiers[i], "r", encoding='utf-8') as fichier:
            texte = fichier.read()

        mots = texte.split()
        mots_check = []

        for k in range(0, len(mots)):
            # Vérifier si un mot n'a pas déjà été analysé dans le même fichier texte
            if mots[k] not in mots_check:
                # Vérifier si le mot est déjà dans un autre fichier
                if mots[k] in dico_IDF.keys():
                    dico_IDF[mots[k]] += 1
                else:
                    dico_IDF[mots[k]] = 1

                # Ajout du mot dans la liste des mots analysés
                mots_check.append(mots[k])

    # Pour chaque mot dans les textes, calcul du poids du mot
    for cle in dico_IDF.keys():
        dico_IDF[cle] = math.log10(1 + (len(fichiers) / (dico_IDF[cle])))

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
        with open(repertoire+fichiers[i], "r", encoding='utf-8') as fichier:
            texte = fichier.read()
            tf = term_frequency(texte)      # Appel de la valeur TF des mots du texte analysé

            # Ajout du score TF-IDF de chaque mot
            for cle_idf in idf.keys():
                if cle_idf not in tf.keys():
                    dico_tf_idf[cle_idf].append(0)

                elif cle_idf in tf.keys():
                    dico_tf_idf[cle_idf].append(idf[cle_idf] * tf[cle_idf])

    return dico_tf_idf


# Fonctionnalités ------------


# Afficher la liste des mots les moins importants dans le corpus de documents
def mots_non_important(repertoire):
    dictionnaire_IDF = Inverse_Document_Frequency(repertoire)  # Appel du score IDF de tous les mots du répertoire
    fichiers = liste_fichiers(repertoire, ".txt") # Appel des noms des fichiers du corpus
    liste_mots_reparti = []     # Triage etape 1
    liste_mots_non_important = []       # Triage final

    # Etape 1: Les mots moins importants sont présents dans la quasi-totalité du corpus => Vérification par le score IDF
    for cle in dictionnaire_IDF.keys():
        IDF_minimal = math.log10(1 + len(fichiers)/(len(fichiers) - 1))
        if dictionnaire_IDF[cle] <= IDF_minimal:
            liste_mots_reparti.append(cle)

    # Etape 2: Les mots moins importants ont un score TF importants dans quasi tous les fichiers du corpus
    TF_mots = {}
    for mot in liste_mots_reparti:              # Appel des mots issus du premier trie
        TF_mots[mot] = []
    for i in range(0, len(fichiers)):
        with open(repertoire + fichiers[i], "r", encoding='utf-8') as fichier:    # Ouverture de chaque texte un par un
            texte = fichier.read()
            tf = term_frequency(texte)  # Appel de la valeur TF des mots du texte analysé

        for cle in tf.keys():
            if cle in TF_mots.keys():
                TF_mots[cle].append(tf[cle])

    # Calcul de la moyenne du TF de chaque mot du premier triage
    for mot in TF_mots.keys():
        moyenne = 0
        for valeur_tf in TF_mots[mot]:
            moyenne = moyenne + valeur_tf
        moyenne = moyenne / len(TF_mots[mot])

        if moyenne > 4:     # Si le mot apparait en moyenne plus de 4 fois par texte
            liste_mots_non_important.append(mot)

    return liste_mots_non_important


# Affiche le nombre de mots importants selon le score TF-IDF demandé par l'utilisateur
def mots_importants(repertoire):
    dictionnaire_TF_IDF = score_tf_idf(repertoire)  # Appel du score TF-IDF de tous les mots du répertoire
    dictionnaire_TF_IDF_max = {}            # Dictionnaire gardant le meilleur score de chaque mot

    liste_mots_important = []

    nb_mots = int(input("Combien de mots importants voulez-vous afficher ? \n"))

    for cle in dictionnaire_TF_IDF.keys():          # Vérification mot par mot des scores TF-IDF

        score_max_mot = 0
        for i in range(0, len(dictionnaire_TF_IDF[cle])):      # Vérification des scores du mot
            if dictionnaire_TF_IDF[cle][i] > score_max_mot:
                score_max_mot = dictionnaire_TF_IDF[cle][i]

        dictionnaire_TF_IDF_max[cle] = score_max_mot       # Ajout du meilleur score du mot dans le dictionnaire

    # Sélections du nombre de "meilleurs" mots demandés par l'utilisateur
    for i in range(0, nb_mots):
        mot_meilleur_score = [0, 0]        # Stocker le mot et le score IDF correspondant dans une liste pour comparer
        for cle in dictionnaire_TF_IDF_max.keys():

            if dictionnaire_TF_IDF_max[cle] > mot_meilleur_score[1]:
                mot_meilleur_score[0] = cle
                mot_meilleur_score[1] = dictionnaire_TF_IDF_max[cle]

        # Mettre le score du mot choisi avant à 0 pour ne pas le reprendre
        dictionnaire_TF_IDF_max[mot_meilleur_score[0]] = 0
        # Ajout du mot au meilleur score dans la liste à retourner
        liste_mots_important.append(mot_meilleur_score[0])

    return liste_mots_important


# Affiche les mots les plus répétés par un président
def mots_plus_utiliser(repertoire):
    fichiers = liste_fichiers(repertoire, ".txt")
    liste_mot_repeter = []
    score_tf_repeter = []

    liste_presidents = extraction_nom(liste_fichiers(repertoire, ".txt"))

    # Demander à l'utilisateur quel président analyser avec saisie sécurisée
    president = 0
    while president not in liste_presidents:
        print("Quel président veux-tu analyser \n: ")
        for noms in liste_presidents:
            print(noms, ", ")
        president = input()

# Demander combien de mots à afficher
    nombre_mots = int(input("Combien de mots ? \n"))

    if "Nomination_"+president+".txt" in fichiers:     # Discours unique du président choisi
        with open(repertoire+"Nomination_"+president+".txt", "r", encoding='utf-8') as fichier:
            texte = fichier.read()
        score_tf = term_frequency(texte)

        # Sélections du nombre de mots le plus répétés demandés par l'utilisateur
        for i in range(0, nombre_mots):
            score_meilleur_mot = [0, 0]  # Stocker le mot et le score TF correspondant dans une liste pour comparer
            for cle in score_tf:

                if score_tf[cle] > score_meilleur_mot[1]:
                    score_meilleur_mot[0] = cle
                    score_meilleur_mot[1] = score_tf[cle]

            # Mettre le score du mot choisi avant à 0 pour ne pas le reprendre
            score_tf[score_meilleur_mot[0]] = 0
            # Ajout du mot au meilleur score dans la liste à retourner
            liste_mot_repeter.append(score_meilleur_mot[0])

        return liste_mot_repeter

    else:                       # Discours 1 et 2 du président choisi

        with open(repertoire+"Nomination_"+president+"1"+".txt", "r", encoding='utf-8') as fichier:     # Discours 1
            texte = fichier.read()
        score_tf = term_frequency(texte)

        # Sélections du nombre de mots le plus répétés demandés par l'utilisateur
        for i in range(0, nombre_mots):
            score_meilleur_mot_1 = [0, 0]  # Stocker le mot et le score TF correspondant dans une liste pour comparer
            for cle in score_tf:

                if score_tf[cle] > score_meilleur_mot_1[1]:
                    score_meilleur_mot_1[0] = cle
                    score_meilleur_mot_1[1] = score_tf[cle]

            # Mettre le score du mot choisi avant à 0 pour ne pas le reprendre
            score_tf[score_meilleur_mot_1[0]] = 0
            liste_mot_repeter.append(score_meilleur_mot_1[0])
            score_tf_repeter.append(score_meilleur_mot_1[1])

        # Discours 2
        with open(repertoire+"Nomination_"+president+"2"+".txt", "r", encoding='utf-8') as fichier:
            texte = fichier.read()
        score_tf = term_frequency(texte)

        # Sélections du nombre de mots le plus répétés demandés par l'utilisateur
        for i in range(0, nombre_mots):
            score_meilleur_mot_2 = [0, 0]  # Stocker le mot et le score TF correspondant dans une liste pour comparer
            for cle in score_tf:

                if score_tf[cle] > score_meilleur_mot_2[1]:
                    score_meilleur_mot_2[0] = cle
                    score_meilleur_mot_2[1] = score_tf[cle]

            # Mettre le score du mot choisi avant à 0 pour ne pas le reprendre
            score_tf[score_meilleur_mot_2[0]] = 0

            # Comparer le TF du mot avec les TF des mots du premier discours, remplacer si supérieur
            k = 0
            while k < len(score_tf_repeter):
                if (score_meilleur_mot_2[1] > score_tf_repeter[len(score_tf_repeter) - k - 1] and
                        score_meilleur_mot_2[0] not in liste_mot_repeter):
                    score_tf_repeter[len(score_tf_repeter) - k - 1] = score_meilleur_mot_2[1]
                    liste_mot_repeter[len(liste_mot_repeter) - k - 1] = score_meilleur_mot_2[0]
                    k = len(score_tf_repeter)
                else:
                    k += 1

        return liste_mot_repeter
