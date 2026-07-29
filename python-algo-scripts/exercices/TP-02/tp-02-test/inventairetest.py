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


def ping(adresse, timeout_s=1):
  option_nombre = "-n" if platform.system() == "Windows" else "-c"
  commande = ["ping", option_nombre, "1", adresse]

  try:
    resultat = subprocess.run(
      commande,
      capture_output=True,
      timeout=timeout_s + 1
    )
    return resultat.returncode == 0
  except subprocess.TimeoutExpired:
    return False


def controler_hotes(hotes, timeout_s):
  resultats = []

  for hote in hotes:
    if "adresse" not in hote:
      logging.warning(f"L'hôte {hote['nom']} n'a pas d'adresse...")
      continue

    joignable = ping(hote["adresse"], timeout_s)

    resultat = {
      "nom": hote["nom"],
      "adresse": hote["adresse"],
      "role": hote["role"],
      "joignable": joignable
    }
    resultats.append(resultat)

    if joignable:
      logging.info(f"Hôte {hote['nom']} ({hote['adresse']}) joignable.")
    else:
      logging.warning(f"Hôte {hote['nom']} ({hote['adresse']}) injoignable.")

  return resultats


def ecrire_rapport(resultats, chemin):
  joignables = 0

  for resultat in resultats:
    if resultat["joignable"]:
      joignables += 1

  rapport = {
    "genere_le": datetime.now(timezone.utc).isoformat(),
    "total": len(resultats),
    "joignables": joignables,
    "injoignables": len(resultats) - joignables,
    "hotes": resultats
  }

  with open(chemin, encoding="utf-8", mode="w") as fichier:
    json.dump(rapport, fichier, indent=2, ensure_ascii=False)

  logging.info(f"Rapport écrit dans {chemin}.")


def charger_hotes(chemin):
  try:
    with open(chemin, encoding="utf-8", mode="r") as fichier:
      donnees = yaml.safe_load(fichier)
      return donnees["hotes"]
  except FileNotFoundError:
    logging.error(f"Le fichier {chemin} est introuvable...")
    sys.exit(1)
  except KeyError:
    logging.error(f"La clé 'hotes' est absente du fichier {chemin}...")
    sys.exit(1)


def analyser_arguments():
  parseur = argparse.ArgumentParser(
    description="Contrôle la disponibilité des machines d'un inventaire YAML."
  )
  parseur.add_argument("--fichier", default="hotes.yaml")
  parseur.add_argument("--rapport", default="rapport.json")
  parseur.add_argument("--log", default="inventaire.log")
  parseur.add_argument("--timeout", type=int, default=1)
  return parseur.parse_args()


def main():
  arguments = analyser_arguments()
  configurer_logging(arguments.log)

  hotes = charger_hotes(arguments.fichier)
  resultats = controler_hotes(hotes, arguments.timeout)
  ecrire_rapport(resultats, arguments.rapport)

  if any(not resultat["joignable"] for resultat in resultats):
    return 2

  return 0


if __name__ == "__main__":
  sys.exit(main())
