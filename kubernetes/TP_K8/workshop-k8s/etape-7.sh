#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export MSYS_NO_PATHCONV=1
k() { kubectl --context=minikube -n stockline "$@"; }
k apply --server-side=false -f workshop-k8s/api-configmap.yaml \
  -f workshop-k8s/api-deployment.yaml -f workshop-k8s/api-service.yaml
k rollout status deployment/api --timeout=180s
k get pods -l app=api
# Contrôler les deux processus, même en l'absence de probes à cette étape.
for pod in $(k get pods -l app=api -o name); do
  k exec "$pod" -- python -c '
import json, time, urllib.request
for attempt in range(20):
    try:
        r=json.load(urllib.request.urlopen("http://127.0.0.1:8000/sante", timeout=2))
        if r["base_de_donnees"] == "ok":
            print(r)
            break
    except OSError:
        pass
    time.sleep(1)
else:
    raise SystemExit("API ou base indisponible apres attente")'
done
k exec sonde -- wget -qO- -T 10 http://api/sante
echo
# N'afficher que les champs non sensibles, jamais DATABASE_URL ni DB_PASSWORD.
k exec deployment/api -- python -c 'import os; print("\n".join(k+"="+os.environ[k] for k in ("DB_HOST","DB_PORT","DB_USER","DB_NAME","DB_SERVICE_HOST","DB_SERVICE_PORT") if k in os.environ)); print("DATABASE_URL et DB_PASSWORD : valeurs masquees")'
# Lire les données avant toute écriture pour éviter les doublons lors d'une reprise.
products=$(k exec sonde -- wget -qO- -T 10 http://api/produits)
echo "$products"
if [[ "$products" != '[]' ]]; then
  echo 'Des produits existent deja : examiner les donnees avant les POST.' >&2
  exit 1
fi
product=$(k exec sonde -- wget -qO- -T 10 --header 'Content-Type: application/json' \
  --post-data '{"reference":"SSD-500","nom":"Disque SSD 500 Go","prix_unitaire":59.9,"seuil_alerte":5}' http://api/produits)
echo "$product"
product_id=$(printf '%s' "$product" | k exec -i deployment/api -- python -c 'import json,sys; print(json.load(sys.stdin)["id"])')
[[ "$product_id" =~ ^[0-9]+$ ]]
k exec sonde -- wget -qO- -T 10 --header 'Content-Type: application/json' \
  --post-data "{\"produit_id\":$product_id,\"type\":\"entree\",\"quantite\":20}" http://api/mouvements
echo
stock=$(k exec sonde -- wget -qO- -T 10 "http://api/stocks/$product_id")
echo "$stock"
printf '%s' "$stock" | k exec -i deployment/api -- python -c 'import json,sys; s=json.load(sys.stdin); assert s["quantite"] == 20 and s["alerte"] is False'
bash workshop-k8s/verifier.sh 7
