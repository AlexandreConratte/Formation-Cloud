import random
 
MOTS = ["hunter",
"fatezero",
"fullmetal",
"bleach",
"parasyte",
"codegeass",
]

def select_world() : 
    
    return random.choice(MOTS)

def choisir_mot():
    
    return random.choice(MOTS)


def creer_affichage(mot, lettres_essayees):
    
    affichage = []

    for lettre in mot:
        if lettre in lettres_essayees:
            affichage.append(lettre)
        else:
            affichage.append("_")

    return " ".join(affichage)


def demander_lettre(lettres_essayees):
    
    while True:
        lettre = input(
          
        ).lower().strip()

        if len(lettre) != 1:
            print("Vous devez entrer une seule lettre.")
        elif not lettre.isalpha():
            print("Vous devez entrer une lettre.")
        elif lettre in lettres_essayees:
            print("Vous avez déjà essayé cette lettre.")
        else:
            return lettre


def jouer():
    mot_a_trouver = choisir_mot()
    lettres_essayees = []
    nombre_de_vies = 7

    while nombre_de_vies > 0:
        mot_affiche = creer_affichage(
            mot_a_trouver,
            lettres_essayees
        )

        print("\n------------------------------")
        print("Nombre de vies restantes :", nombre_de_vies)
        print("Lettres déjà essayées :", lettres_essayees)
        print("Mot à trouver :", mot_affiche)

        if "_" not in mot_affiche:
            print("\nFélicitations !")
            print("Vous avez trouvé le mot :", mot_a_trouver)
            return

        lettre = demander_lettre(lettres_essayees)
        lettres_essayees.append(lettre)

        if lettre in mot_a_trouver:
            print("Bonne réponse !")
        else:
            print("Mauvaise réponse !")
            nombre_de_vies -= 1

    print("\nVous avez perdu !")
    print("Le mot à trouver était :", mot_a_trouver)


jouer()