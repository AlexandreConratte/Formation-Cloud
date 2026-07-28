import json
from pathlib import Path


FICHIER_USERS = Path("users.json")


def charger_users():

    if not FICHIER_USERS.exists():
        sauvegarder_users([])
        return []

    try:
        with open(FICHIER_USERS, "r", encoding="utf-8") as fichier:
            return json.load(fichier)

    except json.JSONDecodeError:
        print("Erreur : le fichier JSON est invalide.")
        return []


def sauvegarder_users(users):
    """Enregistre la liste des utilisateurs dans le fichier JSON."""

    with open(FICHIER_USERS, "w", encoding="utf-8") as fichier:
        json.dump(users, fichier, indent=4, ensure_ascii=False)


def afficher_users(users):
    """Affiche tous les utilisateurs."""

    if not users:
        print("\nAucun utilisateur enregistré.")
        return

    print("\n--- Liste des utilisateurs ---")

    for index, user in enumerate(users, start=1):
        adresse = user["adresse"]

        print(f"""
Utilisateur n°{index}
Nom : {user["nom"]}
Prénom : {user["prenom"]}
Date de naissance : {user["date_naissance"]}
Adresse : {adresse["numero"]} {adresse["voie"]}
          {adresse["code_postal"]} {adresse["commune"]}
Téléphone : {user["telephone"]}
Email : {user["email"]}
--------------------------------
""")


def demander_adresse():
    """Demande les informations concernant une adresse."""

    return {
        "numero": input("Numéro de voie : ").strip(),
        "voie": input("Nom de la voie : ").strip(),
        "code_postal": input("Code postal : ").strip(),
        "commune": input("Commune : ").strip()
    }


def ajouter_user(users):
    """Ajoute un nouvel utilisateur."""

    print("\n--- Ajouter un utilisateur ---")

    user = {
        "nom": input("Nom : ").strip(),
        "prenom": input("Prénom : ").strip(),
        "date_naissance": input(
            "Date de naissance (JJ/MM/AAAA) : "
        ).strip(),
        "adresse": demander_adresse(),
        "telephone": input("Téléphone : ").strip(),
        "email": input("Email : ").strip()
    }

    users.append(user)
    sauvegarder_users(users)

    print("\nUtilisateur ajouté avec succès.")


def choisir_user(users):
    """Demande à l'utilisateur de sélectionner une personne."""

    if not users:
        print("\nAucun utilisateur enregistré.")
        return None

    afficher_users(users)

    try:
        choix = int(input("Numéro de l'utilisateur : "))
        index = choix - 1

        if 0 <= index < len(users):
            return index

        print("Numéro d'utilisateur invalide.")

    except ValueError:
        print("Veuillez saisir un nombre.")

    return None


def modifier_champ(message, ancienne_valeur):
    """
    Permet de conserver l'ancienne valeur
    lorsque l'utilisateur ne saisit rien.
    """

    nouvelle_valeur = input(
        f"{message} [{ancienne_valeur}] : "
    ).strip()

    if nouvelle_valeur == "":
        return ancienne_valeur

    return nouvelle_valeur


def modifier_user(users):
    """Modifie un utilisateur existant."""

    print("\n--- Modifier un utilisateur ---")

    index = choisir_user(users)

    if index is None:
        return

    user = users[index]
    adresse = user["adresse"]

    user["nom"] = modifier_champ("Nom", user["nom"])
    user["prenom"] = modifier_champ("Prénom", user["prenom"])

    user["date_naissance"] = modifier_champ(
        "Date de naissance",
        user["date_naissance"]
    )

    adresse["numero"] = modifier_champ(
        "Numéro de voie",
        adresse["numero"]
    )

    adresse["voie"] = modifier_champ(
        "Nom de la voie",
        adresse["voie"]
    )

    adresse["code_postal"] = modifier_champ(
        "Code postal",
        adresse["code_postal"]
    )

    adresse["commune"] = modifier_champ(
        "Commune",
        adresse["commune"]
    )

    user["telephone"] = modifier_champ(
        "Téléphone",
        user["telephone"]
    )

    user["email"] = modifier_champ(
        "Email",
        user["email"]
    )

    sauvegarder_users(users)

    print("\nUtilisateur modifié avec succès.")


def supprimer_user(users):
    """Supprime un utilisateur."""

    print("\n--- Supprimer un utilisateur ---")

    index = choisir_user(users)

    if index is None:
        return

    user = users[index]

    confirmation = input(
        f"Supprimer {user['prenom']} {user['nom']} ? (o/n) : "
    ).strip().lower()

    if confirmation == "o":
        users.pop(index)
        sauvegarder_users(users)
        print("\nUtilisateur supprimé.")
    else:
        print("\nSuppression annulée.")


def afficher_menu():
    print("""
=============================
     GESTION UTILISATEURS
=============================
1 - Afficher les utilisateurs
2 - Ajouter un utilisateur
3 - Modifier un utilisateur
4 - Supprimer un utilisateur
0 - Quitter
=============================
""")


def main():
    users = charger_users()

    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip()

        match choix:
            case "1":
                afficher_users(users)

            case "2":
                ajouter_user(users)

            case "3":
                modifier_user(users)

            case "4":
                supprimer_user(users)

            case "0":
                print("\nFermeture du programme.")
                break

            case _:
                print("\nChoix invalide.")


if __name__ == "__main__":
    main()