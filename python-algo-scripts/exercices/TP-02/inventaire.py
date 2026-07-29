import sys
import subprocess
import yaml
from pathlib import Path
import platform
from datetime import datetime, timezone
import json



FICHIER_USERS = Path(__file__).resolve().parent / "hotes.yaml"

#print(FICHIER_USERS)

def charger_hotes(chemin):
  try:
    with open(chemin, encoding="utf-8", mode="r") as fichier:
      donnees = yaml.safe_load(fichier)
      return donnees["hotes"]
  except FileNotFoundError:
    print(f"Fichier {chemin} introuvable...")
    sys.exit(1)
  except KeyError:
    print(f"Clé 'hotes' absente du fichier {chemin}")
    sys.exit(1)





def ping(adresse, timeout_s=1): 

    
    option_system = "-n" if platform.system() == "Windows" else "-c"
    commande = ["ping", option_system, "1", adresse]
    
    try  :
        res = subprocess.run(commande, capture_output=True, timeout= timeout_s + 1)   
        return res.returncode ==0 
   
    except subprocess.TimeoutExpired : 
        return False

# Test du PING dans le REPL : 
# Administrateur@Salle3-3-1 MINGW64 ~/OneDrive - M2I/Bureau/.repos/Formation-Cloud/python-algo-scripts/exercices/TP-02 (main)
# $ python
# Python 3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# Ctrl click to launch VS Code Native REPL
# >>> from inventaire import ping
# >>> ping("127.0.0.1")
# True
# >>> ping("192.0.2.1")
# True
# >>> ping("192.0.2.1")
# False
# >>>      

    
def controler_hotes(hotes, timeout_s) : 

    rendu_controler_hotes=[]
 
    for hote in hotes:
     
     if "adresse" not in hote:
       print(f"Avertissement : l'hôte {hote['nom']} n'a pas d'adresse !! ")
       continue
 
     dictionnaire = {
       "nom": hote["nom"],
       "adresse": hote["adresse"],
       "role": hote["role"],
       "joignable": ping(hote["adresse"], timeout_s)
     }
     rendu_controler_hotes.append(dictionnaire)
 
    return rendu_controler_hotes

def ecrire_rapport(resultats, chemin) : 

    nbr_hotes_joignables = 0

    for resultat in resultats:
        if resultat["joignable"]:
          nbr_hotes_joignables += 1
    
        rapport = {
        "genere_le": datetime.now(timezone.utc).isoformat(),
        "total": len(resultats),
        "joignables": nbr_hotes_joignables,
        "injoignables": len(resultats) - nbr_hotes_joignables,
        "hotes": resultats
      }
        

    with chemin.open("w", encoding="utf-8") as fichier:
           json.dump(rapport, fichier, indent=2, ensure_ascii=False)




def main():
  hotes = charger_hotes(FICHIER_USERS)
  #print(hotes)
  resultats = controler_hotes(hotes, 1)
  ecrire_rapport(resultats, "rapport.json")
#  for hote in hotes:
#    print(hote["nom"])



if __name__ == "__main__":
  main()