import os
import math


# Fonctions analyse texte
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

                    # Remplacer les ponctuations par un blanc
                    if ord(caractere) in liste_ponctuation_retrait:
                        fichier.write("")

                    # Remplacer "-"  par un espace
                    elif ord(caractere) == 45:
                        fichier.write(" ")
                    # Remplacer les apostrophe par "e "
                    elif ord(caractere) == 39:
                        fichier.write("e ")
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


# fonction pour déterminer un dictionnaire avec chaque mot associé à son occurrence
def term_frequency(chaine):
    # Diviser la chaine de caractère en une liste de mots
    mots = chaine.split()
    dico_tf = {}     # dictionnaire
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
            dico_tf[mots[i]] = occurrence

    return dico_tf


def inverse_document_frequency(repertoire):
    dico_idf = {}
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
                if mots[k] in dico_idf.keys():
                    dico_idf[mots[k]] += 1
                else:
                    dico_idf[mots[k]] = 1

                # Ajout du mot dans la liste des mots analysés
                mots_check.append(mots[k])

    # Pour chaque mot dans les textes, calcul du poids du mot
    for cle in dico_idf.keys():
        dico_idf[cle] = math.log10((len(fichiers) / (dico_idf[cle])))

    return dico_idf


def score_tf_idf(repertoire):
    dico_tf_idf = {}
    fichiers = liste_fichiers(repertoire, ".txt")

    # Appeler la valeur IDF de chacun des mots dans les textes du répertoire
    idf = inverse_document_frequency(repertoire)

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
    dictionnaire_idf = inverse_document_frequency(repertoire)  # Appel du score IDF de tous les mots du répertoire
    fichiers = liste_fichiers(repertoire, ".txt")    # Appel des noms des fichiers du corpus
    liste_mots_reparti = []     # Triage etape 1
    liste_mots_non_important = []       # Triage final

# Etape 1 : Les mots moins importants sont présents dans la quasi-totalité du corpus => Vérification par le score IDF
    for cle in dictionnaire_idf.keys():
        idf_minimal = math.log10(1 + len(fichiers)/(len(fichiers) - 1))
        if dictionnaire_idf[cle] <= idf_minimal:
            liste_mots_reparti.append(cle)

    # Etape 2 : Les mots moins importants ont un score TF importants dans quasi tous les fichiers du corpus
    tf_mots = {}
    for mot in liste_mots_reparti:              # Appel des mots issus du premier trie
        tf_mots[mot] = []
    for i in range(0, len(fichiers)):
        with open(repertoire + fichiers[i], "r", encoding='utf-8') as fichier:    # Ouverture de chaque texte un par un
            texte = fichier.read()
            tf = term_frequency(texte)  # Appel de la valeur TF des mots du texte analysé

        for cle in tf.keys():
            if cle in tf_mots.keys():
                tf_mots[cle].append(tf[cle])

    # Calcul de la moyenne du TF de chaque mot du premier triage
    for mot in tf_mots.keys():
        moyenne = 0
        for valeur_tf in tf_mots[mot]:
            moyenne = moyenne + valeur_tf
        moyenne = moyenne / len(tf_mots[mot])

        if moyenne > 4:     # Si le mot apparait en moyenne plus de 4 fois par texte
            liste_mots_non_important.append(mot)

    return liste_mots_non_important


# Affiche le nombre de mots importants selon le score TF-IDF demandé par l'utilisateur
def mots_importants(repertoire):
    dictionnaire_tf_idf = score_tf_idf(repertoire)  # Appel du score TF-IDF de tous les mots du répertoire
    dictionnaire_tf_idf_max = {}            # Dictionnaire gardant le meilleur score de chaque mot

    liste_mots_important = []

    # Saisie sécurisée
    nb_mots = input("Combien de mots au score TF-IDF élevé voulez-vous afficher ? \n")
    while type(nb_mots) is not int:
        try:
            nb_mots = int(nb_mots)
            while nb_mots < 0:
                nb_mots = input("Veuillez entrer un entier positif : \n")
        except TypeError:
            nb_mots = input("Veuillez entrer un nombre entier \n")
        except ValueError:
            nb_mots = input("Veuillez entrer un nombre entier \n")

    for cle in dictionnaire_tf_idf.keys():          # Vérification mot par mot des scores TF-IDF

        score_max_mot = 0
        for i in range(0, len(dictionnaire_tf_idf[cle])):      # Vérification des scores du mot
            if dictionnaire_tf_idf[cle][i] > score_max_mot:
                score_max_mot = dictionnaire_tf_idf[cle][i]

        dictionnaire_tf_idf_max[cle] = score_max_mot       # Ajout du meilleur score du mot dans le dictionnaire

    # Sélections du nombre de "meilleurs" mots demandés par l'utilisateur
    for i in range(0, nb_mots):
        mot_meilleur_score = [0, 0]        # Stocker le mot et le score IDF correspondant dans une liste pour comparer
        for cle in dictionnaire_tf_idf_max.keys():

            if dictionnaire_tf_idf_max[cle] > mot_meilleur_score[1]:
                mot_meilleur_score[0] = cle
                mot_meilleur_score[1] = dictionnaire_tf_idf_max[cle]

        # Mettre le score du mot choisi avant à 0 pour ne pas le reprendre
        dictionnaire_tf_idf_max[mot_meilleur_score[0]] = 0
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
    nombre_mots = input("Combien de mots ? \n")
    while type(nombre_mots) is not int:
        try:
            nombre_mots = int(nombre_mots)
            while nombre_mots < 0:
                nombre_mots = input("Veuillez entrer un entier positif : \n")
        except TypeError:
            nombre_mots = input("Veuillez entrer un nombre entier \n")
        except ValueError:
            nombre_mots = input("Veuillez entrer un nombre entier \n")

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


#  affiche les noms des présidents qui ont parlé d'un mot et donne le nombre de fois qu'ils l'ont dit
def stat_mot(repertoire):
    liste_noms_fichier = liste_fichiers(repertoire, ".txt")
    nbr_mot_president = {}
    mot_demande = input("Entrez le mot a rechercher : ")

    for nom in extraction_nom(liste_noms_fichier):  # determiner quels presidents a parle du mot

        if nom == "Chirac" or nom == "Mitterrand":  # pour les presidents qui ont deux discours
            with open("cleaned/" + "Nomination_" + nom + "1" + ".txt", "r", encoding='utf-8') as fichier:
                texte = fichier.read()

                if mot_demande in texte:  # determiner quels presidents a parle du mot
                    dico = term_frequency(texte)
                    for cle in dico.keys():
                        if cle == mot_demande:
                            # ajoute le nombre de fois que le mot a été prononcé
                            nbr_mot_president[nom] = dico[cle]
                    presidentbis = 1  # pour signifier que le premier discours contient le mot
                else:
                    presidentbis = 0

            with open("cleaned/" + "Nomination_" + nom + "2" + ".txt", "r", encoding='utf-8') as fichier:
                texte = fichier.read()
                if mot_demande in texte:  # determiner quels presidents a parle du mot
                    dico = term_frequency(texte)
                    for cle in dico.keys():
                        if cle == mot_demande:
                            if presidentbis == 0:
                                nbr_mot_president[nom] = dico[cle]  # ajoute le nombre de fois que le mot a été prononcé
                            elif presidentbis == 1:
                                for key in nbr_mot_president.keys():
                                    if key == nom:
                                        nbr_mot_president[key] = dico[cle] + nbr_mot_president[key]

        else:  # pour les presidents n'ayant qu'un discours
            with open("cleaned/" + "Nomination_" + nom + ".txt", "r", encoding='utf-8') as fichier:
                texte = fichier.read()
                if mot_demande in texte:
                    dico = term_frequency(texte)
                    for cle in dico.keys():
                        if cle == mot_demande:
                            nbr_mot_president[nom] = dico[cle]  # ajoute le nombre de fois que le mot a été prononcé
    if nbr_mot_president == {}:
        return "Aucun président n'a utilisé ce mot"
    else:
        return nbr_mot_president


# fonctionnalité donnant le premier president à parler d'un mot
def premier_president(repertoire):
    mot_cherche = input("donner le mot à rechercher : ")
    liste_noms_fichier = liste_fichiers(repertoire, ".txt")
    rapid = {}
    for nom in extraction_nom(liste_noms_fichier):
        if nom == "Chirac" or nom == "Mitterrand":  # pour les presidents qui ont deux discours
            # premier discours
            with open("cleaned/" + "Nomination_" + nom + "1" + ".txt", "r", encoding='utf-8') as fichier:
                texte = fichier.read()
                if mot_cherche in texte:  # vérifier que le mot soit dans le texte
                    mots = texte.split()
                    i = 0
                    while mots[i] != mot_cherche and i < (len(mots)-1):  # trouver le rang du mot
                        i += 1
                    if i < len(mots):  # sécurité si le mot n'y est pas
                        rapid[nom] = i  # mettre le rang dans un dictionnaire
            # deuxième discours
            with open("cleaned/" + "Nomination_" + nom + "1" + ".txt", "r", encoding='utf-8') as fichier:
                texte = fichier.read()
                if mot_cherche in texte:  # vérifier que le mot soit dans le texte
                    mots = texte.split()
                    i = 0
                    while mots[i] != mot_cherche and i < (len(mots)-1):  # trouver le rang du mot
                        i += 1
                    if i < len(mots):  # sécurité si le mot n'y est pas
                        rapid[nom] = i  # mettre le rang dans un dictionnaire

        else:  # pour les presidents n'ayant qu'un discours
            with open("cleaned/" + "Nomination_" + nom + ".txt", "r", encoding='utf-8') as fichier:
                texte = fichier.read()
                if mot_cherche in texte:  # vérifier que le mot soit dans le texte
                    mots = texte.split()
                    i = 0
                    while mots[i] != mot_cherche and i < (len(mots)-1):  # trouver le rang du mot
                        i += 1
                    if i < len(mots):  # sécurité si le mot n'y est pas
                        rapid[nom] = i  # mettre le rang dans un dictionnaire

    if rapid == {}:  # cas où aucun président n'a parlé de ce mot
        return "Aucun président n'a dit ce mot."
    else:
        best = 9999999999999
        for cle in rapid:  # détermine quel président a parlé du mot le plus rapidement
            if rapid[cle] < best:
                best = rapid[cle]
                bestpresident = cle
        return bestpresident, "a dit ce mot le plus vite dans son discours."


# fonctionnalité qui donne les mots prononcés par tous les présidents qui ne sont pas des mots "non important"
def mot_commun(repertoire):
    liste_noms_fichier = liste_fichiers(repertoire, ".txt")
    list_mots = []  # liste des listes de tous les mots
    for nom in extraction_nom(liste_noms_fichier):
        if nom == "Chirac" or nom == "Mitterrand":  # pour les presidents qui ont deux discours
            with open("cleaned/" + "Nomination_" + nom + "1" + ".txt", "r", encoding='utf-8') as fichier:
                # premier discours
                texte = fichier.read()
                list_mots.append(texte.split())  # ajoute la liste des mots dans la liste complète
            # deuxième discours
            with open("cleaned/" + "Nomination_" + nom + "2" + ".txt", "r", encoding='utf-8') as fichier:
                texte = fichier.read()
                list_mots.append(texte.split())  # ajoute la liste des mots dans la liste complète
        else:  # pour les presidents n'ayant qu'un discours
            with open("cleaned/" + "Nomination_" + nom + ".txt", "r", encoding='utf-8') as fichier:
                texte = fichier.read()
                list_mots.append(texte.split())  # ajoute la liste des mots dans la liste complète
    liste_mots_lambda = mots_non_important(repertoire)
    liste_mot_commun = set()  # set des mots prononcés par tous les présidents
    for mot in list_mots[0]:
        cpt = 0  # compteur pour vérifier que le mot soit dans tou les discours
        for i in range(1, len(list_mots)):
            if mot in list_mots[i]:
                cpt += 1  # incrémentation pour chaque texte dans lequel le mot est

        if cpt == 7:
            if mot not in liste_mots_lambda:  # vérifier que ce n'est pas un mon pas important
                liste_mot_commun.add(mot)  # ajouter les mots dit par tous les présidents à la liste
    return liste_mot_commun

# question réponse ------------


# Fonctions analyse questions
def mots_questions(question):
    question_minuscule = ""
    question_clean = ""

    # Conversion minuscule
    for mot in question:
        for caractere in mot:
            if ord(caractere) >= 65 and ord(caractere) <= 90:
                question_minuscule = question_minuscule + chr(ord(caractere) + 32)
            else:
                question_minuscule = question_minuscule + caractere

    # Retrait des ponctuations
    for mot in question_minuscule:
        for caractere in mot:

            # Code ASCII des ponctuations
            liste_ponctuation_retrait = [33, 34, 44,
                                         46, 58, 59, 63,
                                         96, 130, 132,
                                         133, 145, 146,
                                         147, 148, 149,
                                         ]

            # Remplacer les ponctuations par un blanc
            if ord(caractere) in liste_ponctuation_retrait:
                question_clean += ""

            # Remplacer "-"  par un espace
            elif ord(caractere) == 45:
                question_clean += " "
            # Remplacer les apostrophe par "e "
            elif ord(caractere) == 39:
                question_clean += "e "
            else:
                question_clean += caractere

    liste_mot_question = question_clean.split(" ")

    return liste_mot_question


# Fonctions identification des mots et dans la question et dans le corpus de documents
def correspondance_question_textes(liste_mot_question):
    fichiers = liste_fichiers("cleaned/", ".txt")
    mots_dans_texte = set()

    for i in range(0, len(fichiers)):

        # Lecture du fichier texte
        with open("cleaned/" + fichiers[i], "r", encoding='utf-8') as fichier:
            texte = fichier.read()
            mots_texte = texte.split()

        for mot in liste_mot_question:
            if mot in mots_texte:
                mots_dans_texte.add(mot)

    # Si la liste est vide, donc s'il n'y a aucun mot de la question dans le corpus
    if mots_dans_texte == set():
        return "oops"
    else:
        return mots_dans_texte


# TF-IDF de la question
def tf_idf_question(question):
    # Appel des valeurs IDF de tous les mots du corpus ET de la liste des mots dans le corpus
    idf = inverse_document_frequency("cleaned/")

    liste_mot_question = mots_questions(question)
    mots_dans_texte = correspondance_question_textes(liste_mot_question)

    question_minuscule = ""  # Concaténation des mots en minuscule et sans ponctuation de la question
    for mot in liste_mot_question:
        question_minuscule = question_minuscule + " " + mot

    tf_mots = {}
    tf_idf_mots = {}

    # Calcul du TF de chaque mot du corpus dans la question
    tf_question = term_frequency(question_minuscule)

    for key in idf.keys():  # Appeler tous les mots du corpus
        if key not in liste_mot_question:  # Si mot du corpus absent de la question, TF = 0
            tf_mots[key] = 0.0

        elif key in liste_mot_question:  # Si mot du corpus dans la question

            for mot in tf_question.keys():
                if mot in mots_dans_texte:  # Si mot de la question dans le corpus, ajout du TF du mot dans la question
                    tf_mots[mot] = tf_question[mot]

    # Calcul IDF de chaque mot du corpus dans la question
    for mot in tf_mots:
        tf_idf_mots[mot] = tf_mots[mot] * idf[mot]  # Produit des TF dans la question et des IDF de chaque mot = TF-IDF

    return tf_idf_mots


# Fonction produit scalaire
def produit_scalaire(vecteur_a, vecteur_b):
    if len(vecteur_a) == len(vecteur_b):
        produit = 0
        nb_valeurs = len(vecteur_a)

        for i in range(0, nb_valeurs):
            produit += vecteur_a[i] * float(vecteur_b[i])

        return produit
    else:
        return "Erreur Vecteur de taille différente !"


# Fonction norme de vecteur
def norme_vecteur(vecteur):
    norme_carre = 0
    for i in range(0, len(vecteur)):
        norme_carre += vecteur[i] * vecteur[i]
    norme = math.sqrt(norme_carre)

    return norme


# Fonction calcul similarité
def calcul_similarite(vecteur_a, vecteur_b):
    if len(vecteur_a) == len(vecteur_b):
        # Appel du produit scalaire de A et B, et leur norme respective
        produit_a_b = produit_scalaire(vecteur_a, vecteur_b)
        norme_a = norme_vecteur(vecteur_a)
        norme_b = norme_vecteur(vecteur_b)

        similarite = produit_a_b / norme_a * norme_b
        return float(similarite)
    else:
        return "oups"


# Calcul Document le plus pertinent
def doc_pertinence(tf_idf_corpus, tf_idf_q, liste_nom_fichiers, question):
    best_doc = 0
    nb_vecteur_corpus = len(liste_nom_fichiers)
    meilleur = 0

    mot_important = mot_tf_idf(question)

    present = False
    for i in range(0, nb_vecteur_corpus):

        # Vérification de la présence du mot important dans le document à comparer
        with open("cleaned/" + liste_nom_fichiers[i], "r", encoding='utf-8') as fichier:
            texte = fichier.read()

        texte_mots = texte.split()

        for j in range(0, len(texte_mots)):

            if texte_mots[j] == mot_important:
                present = True
                vecteur_document = []

                # Remplissage d'une liste = vecteur TF_IDF du i-ième document du corpus
                for k in range(0, len(tf_idf_corpus)):
                    vecteur_document.append(tf_idf_corpus[k][i])

                # Calcul pour trouver le document le plus similaire à la question
                cpt = calcul_similarite(tf_idf_q, vecteur_document)

                if cpt >= meilleur:
                    meilleur = cpt
                    best_doc = i
    if present == True:
        nom_doc = liste_nom_fichiers[best_doc]
        return nom_doc
    else:
        return "absent"


def mot_tf_idf(question):
    tf_idf = tf_idf_question(question)

    best = 0
    best_mot = ""
    # on parcourt les mots du dictionnaire tf_idf
    for cle in tf_idf.keys():
        # on regarde quel mot a le meilleur tf_idf
        if tf_idf[cle] > best:
            best = tf_idf[cle]
            best_mot = cle
    return best_mot


# récupérer la première phrase qui contient le mot dans le fichier
def reponse(mot_important, nom_doc):
    if nom_doc == "absent":
        return "Désolé, je ne peux répondre. Pouvez-vous reformuler ?"
    else:
        with open("speeches/" + nom_doc, "r", encoding='utf-8') as fichier:
            texte = fichier.readlines()

        trouvee = False

        i = 0
        while trouvee == False and i < len(texte):
            phrase_brut = texte[i]
            # Retrait saut de ligne
            phrase_liste_mot = phrase_brut.split("\n")
            phrase = phrase_liste_mot[0]
            # Conserver la phrase
            phrase_original = phrase
            # Retrait point final
            phrase_liste_mot = phrase.split(".")
            phrase = phrase_liste_mot[0]
            # Retrait autre ponctuation
            phrase_sans_ponctuation = ""
            for caractere in phrase:

                if caractere == ",":
                    phrase_sans_ponctuation += ""
                elif ord(caractere) == 45:
                    phrase_sans_ponctuation += " "
                elif ord(caractere) == 39:
                    phrase_sans_ponctuation += "e "
                else:
                    phrase_sans_ponctuation += caractere

            phrase_sans_ponctuation_liste = phrase_sans_ponctuation.split()

            if mot_important in phrase_sans_ponctuation_liste:
                trouvee = True

            else:
                i += 1
        return phrase_original


def politesse(phrase, question):
    if "Comment" in question:
        phrase = "Après analyse : " + phrase
    elif "Peux-tu" in question:
        phrase = "Oui, bien sûr ! " + phrase

    return phrase
