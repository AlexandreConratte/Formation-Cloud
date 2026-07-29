import argparse
import json
import logging
import platform
import subprocess
import sys
from datetime import datetime, timezone

import yaml


def configurer_logging(chemin):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(chemin, encoding="utf-8")
        ],
        force=True
    )


def charger_hotes(chemin):
    try:
        with open(chemin, encoding="utf-8", mode="r") as fichier:
            donnees = yaml.safe_load(fichier)
            return donnees["hotes"]
    except FileNotFoundError:
        logging.error(f"Fichier {chemin} introuvable...")
        sys.exit(1)
    except KeyError:
        logging.error(f"Clé 'hotes' absente du fichier {chemin}...")
        sys.exit(1)
    except yaml.YAMLError:
        logging.error(f"Le fichier YAML {chemin} est invalide...")
        sys.exit(1)


def ping(adresse, timeout_s=1):
    option_systeme = "-n" if platform.system() == "Windows" else "-c"
    commande = ["ping", option_systeme, "1", adresse]

    try:
        resultat_ping = subprocess.run(
            commande,
            capture_output=True,
            timeout=timeout_s + 1
        )
        return resultat_ping.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def controler_hotes(hotes, timeout_s):
    resultats_controler_hotes = []

    for hote in hotes:
        if "adresse" not in hote:
            logging.warning(
                f"L'hôte {hote['nom']} n'a pas d'adresse."
            )
            continue

        joignable = ping(hote["adresse"], timeout_s)

        dictionnaire_hote = {
            "nom": hote["nom"],
            "adresse": hote["adresse"],
            "role": hote["role"],
            "joignable": joignable
        }
        resultats_controler_hotes.append(dictionnaire_hote)

        if joignable:
            logging.info(f"Hôte {hote['nom']} ({hote['adresse']}) joignable.")
        else:
            logging.warning(f"Hôte {hote['nom']} ({hote['adresse']}) injoignable.")

    return resultats_controler_hotes


def ecrire_rapport(resultats, chemin):
    nbr_hotes_joignables = 0

    for statut in resultats:
        if statut["joignable"]:
            nbr_hotes_joignables += 1

    rapport = {
        "genere_le": datetime.now(timezone.utc).isoformat(),
        "total": len(resultats),
        "joignables": nbr_hotes_joignables,
        "injoignables": len(resultats) - nbr_hotes_joignables,
        "hotes": resultats
    }

    with open(chemin, encoding="utf-8", mode="w") as fichier:
        json.dump(rapport, fichier, indent=2, ensure_ascii=False)

    logging.info(f"Rapport écrit dans {chemin}.")


def analyser_arguments():
    parseur = argparse.ArgumentParser(
        description="Contrôle la disponibilité des machines d'un inventaire YAML."
    )
    parseur.add_argument(
        "--fichier",
        default="hotes.yaml",
        help="fichier YAML d'inventaire (hotes.yaml)"
    )
    parseur.add_argument(
        "--rapport",
        default="rapport.json",
        help="fichier JSON de sortie (rapport.json)"
    )
    parseur.add_argument(
        "--log",
        default="inventaire.log",
        help="fichier de log (inventaire.log)"
    )
    parseur.add_argument(
        "--timeout",
        type=int,
        default=1,
        help="ping (timeout_s = 1)"
    )
    return parseur.parse_args()


def main():
    arguments = analyser_arguments()
    configurer_logging(arguments.log)

    hotes = charger_hotes(arguments.fichier)
    resultats = controler_hotes(hotes, arguments.timeout)
    ecrire_rapport(resultats, arguments.rapport)

    for resultat in resultats:
        if not resultat["joignable"]:
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
