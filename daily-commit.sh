#!/bin/bash

# Se placer dans le dossier du repository
cd ~/devOps/Formation-Cloud || exit 1

# Ajouter une entrée au journal
echo "$(date '+%Y-%m-%d %H:%M:%S') - Daily DevOps activity" >> devops-log.txt

# Ajouter la modification à Git
git add devops-log.txt

# Créer le commit
git commit -m "chore: daily DevOps activity"

# Envoyer sur GitHub
git push origin main