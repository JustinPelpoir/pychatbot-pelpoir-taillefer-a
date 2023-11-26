# l'historique des modification n'est pas complet dans l'historique des commit. Il faut regarder l'historique des activités pour voir l'ensemble des modifications.
from functions import *

fichiers = liste_fichiers("speeches", ".txt")

conversion_minuscule(fichiers)

retrait_ponctuation(fichiers)
score_tf_idf("cleaned/")


# Menu -------------
a = 0  # Etat "On"
while a == 0:
    print("===== ChatBot : v0.1 =====\n"
          "Ce Chatbot est en cours de développement, des bugs sont susceptibles de se produire.\n\n"
          "----------\n"      
          "Menu :  Pour accéder à une fonctionnalité, entrez le numéro qui lui est associé\n\n"
          "1: Afficher la liste des mots les moins importants dans le corpus\n"
          "2: Afficher le(s) mot(s) ayant le score TF-IDF le plus élevé(s)\n"
          "3: Afficher le(s) mot(s) le(s) plus répété(s) par un président\n"
          "4: Indiquer le(s) nom(s) du (des) président(s) qui a "
          "(ont) utilisé un mot et combien de fois il(s) l'a(ont) répété \n"
          "5: Indiquer le premier président à parler de quelque chose\n"
          "6: Indiquer quel(s) est(sont) le(s) mot(s) que tous les présidents ont évoqués\n\n"
          "0: Fermer le Chatbot\n\n"
          )

    choix = input("Votre choix : ")
    while type(choix) is not int:  # saisie sécurisée
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
        while type(x) is not int:  # saisie sécurisée
            try:
                x = int(x)
            except ValueError:
                x = input("Êtes-vous sûr de vouloir fermer le Chatbot ? 1: Oui ; 2: Non : \n")
        if x == 1:
            a = 1       # Etat "Off"

    if choix != 0:
        choix = input("Retour au menu ? 1: Oui ; 2: Non\n")
        while type(choix) is not int:  # saisie sécurisée
            try:
                choix = int(choix)
            except ValueError:
                choix = input("Retour au menu ? 1: Oui ; 2: Non\n")

        if choix == 2:
            x = input("Êtes-vous sûr de vouloir fermer le Chatbot ? 1: Oui ; 2: Non : \n")
            while type(x) is not int:  # saisie sécurisée
                try:
                    x = int(x)
                except ValueError:
                    x = input("Êtes-vous sûr de vouloir fermer le Chatbot ? 1: Oui ; 2: Non : \n")
            if x == 1:
                a = 1           # Etat "Off"
