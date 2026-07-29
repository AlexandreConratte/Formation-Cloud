import json
import platform
import subprocess
import sys
from datetime import datetime, timezone

import yaml


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
      print(f"Avertissement : l'hôte {hote['nom']} n'a pas d'adresse...")
      continue

    resultat = {
      "nom": hote["nom"],
      "adresse": hote["adresse"],
      "role": hote["role"],
      "joignable": ping(hote["adresse"], timeout_s)
    }
    resultats.append(resultat)

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


def charger_hotes(chemin):
  try:
    with open(chemin, encoding="utf-8", mode="r") as fichier:
      donnees = yaml.safe_load(fichier)
      return donnees["hotes"]
  except FileNotFoundError:
    print(f"Le fichier {chemin} est introuvable...")
    sys.exit(1)
  except KeyError:
    print(f"La clé 'hotes' est absente du fichier {chemin}...")
    sys.exit(1)


def main():
  hotes = charger_hotes("hotes.yaml")
  resultats = controler_hotes(hotes, 1)
  ecrire_rapport(resultats, "rapport.json")


if __name__ == "__main__":
  main()
