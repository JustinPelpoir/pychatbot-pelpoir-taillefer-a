# My First ChatBot, PELPOIR Justin TAILLEFER Victor 
# Mise en place du menu et mise en place de l'utilisation des fonctions et fonctionnalités. 

from functions import *

fichiers = liste_fichiers("speeches", ".txt")

conversion_minuscule(fichiers)

retrait_ponctuation(fichiers)

tfidf_corpus = score_tf_idf("cleaned/")

fichiers_clean = liste_fichiers("cleaned/", ".txt")


# Menu -------------

a = 0  # Etat "On"
print("===== ChatBot : v0.2 =====\n"
          "Ce Chatbot est en cours de développement, des bugs sont susceptibles de se produire.\n\n"
          "----------\n"
      )
while a == 0:

    # sélectionner le mode
    print("Pour accéder au différente fonctionnalités, entrez : 1\n"
            "Pour poser des questions au chatbot, entrez : 2\n\n"
            "Pour quitter le chatbot, entrez : 0"
          )
    z = input("Votre choix : ")
    while type(z) is not int and ((z != 1) or (z != 2)):
        try:
            z = int(z)
        except ValueError:
            z = input("Votre choix : ")

    # Menu : Fonctionnalités
    if z == 1:

        print("\n\n\n"
            "Menu :  Pour accéder à une fonctionnalité, entrez le numéro qui lui est associé\n\n"
            "1: Afficher la liste des mots les moins importants dans le corpus\n"
            "2: Afficher le(s) mot(s) les plus importants\n"
            "3: Afficher le(s) mot(s) le(s) plus répété(s) par un président\n"
            "4: Indiquer le(s) nom(s) du (des) président(s) qui a "
            "(ont) utilisé un mot et combien de fois il(s) l'a(ont) répété \n"
            "5: Indiquer le premier président à parler de quelque chose\n"
            "6: Indiquer quel(s) est(sont) le(s) mot(s) que tous les présidents ont évoqués\n\n"
            "0: Fermer le Chatbot\n\n"
            )

        choix = input("Votre choix : ")
        while type(choix) is not int:
            try:
                choix = int(choix)
            except ValueError:
                choix = input("Votre choix : ")

        if choix == 1:
            print(mots_non_important("cleaned/"))
        elif choix == 2:
            print(mots_importants("cleaned/"))
        elif choix == 3:
            print(mots_plus_utiliser("cleaned/"))
        elif choix == 4:
            print(stat_mot("cleaned/"))
        elif choix == 5:
            print(premier_president("cleaned/"))
        elif choix == 6:
            print(mot_commun("cleaned/"))

        elif choix == 0:
            x = input("Êtes-vous sûr de vouloir fermer le Chatbot ? 1: Oui ; 2: Non : ")
            while type(x) is not int:
                try:
                    x = int(x)
                except ValueError:
                    x = input("Êtes-vous sûr de vouloir fermer le Chatbot ? 1: Oui ; 2: Non : \n")
            if x == 1:
                a = 1  # Etat "Off"

        if choix != 0:
            choix = input("Retour au menu ? 1: Oui ; 2: Non\n")
            while type(choix) is not int:
                try:
                    choix = int(choix)
                except ValueError:
                    choix = input("Retour au menu ? 1: Oui ; 2: Non\n")

            if choix == 2:
                x = input("Êtes-vous sûr de vouloir fermer le Chatbot ? 1: Oui ; 2: Non : \n")
                while type(x) is not int:
                    try:
                        x = int(x)
                    except ValueError:
                        x = input("Êtes-vous sûr de vouloir fermer le Chatbot ? 1: Oui ; 2: Non : \n")
                if x == 1:
                    a = 1  # etat "Off"

    # Menu : Question
    if z == 2:
        # Question
        j = 0
        print("Posez votre question : ")
        while j == 0:
            question = input()
            tf_idf_q = tf_idf_question(question)

            # Conversion dictionnaire - Vecteur/liste
            tf_idf_q_liste = []
            tfidf_corpus_liste = []
            for mot in tfidf_corpus:
                tfidf_corpus_liste.append(tfidf_corpus[mot])
            for mot in tf_idf_q:
                tf_idf_q_liste.append(tf_idf_q[mot])

            # Traitement de la question
            try:
                print(politesse(
                    reponse(mot_tf_idf(question),
                            doc_pertinence(tfidf_corpus_liste, tf_idf_q_liste, fichiers_clean, question)),
                    question), "\n\n")
                j = 1

            except ZeroDivisionError:
                print("Désolé, je n'ai pas compris votre question. Pouvez-vous répéter ? \n")

    # Coupure
    if z == 0:
        a = 1
