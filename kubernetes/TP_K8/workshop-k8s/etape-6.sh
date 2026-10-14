#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export MSYS_NO_PATHCONV=1
k() { kubectl --context=minikube -n stockline "$@"; }
command -v openssl >/dev/null
existing=$(k get secret db-credentials --ignore-not-found -o name)
if [[ -z "$existing" ]]; then
  password=$(openssl rand -hex 16)
  k create secret generic db-credentials \
    --from-literal=POSTGRES_USER=stockline \
    --from-literal=POSTGRES_PASSWORD="$password" \
    --from-literal=POSTGRES_DB=stockline
  unset password
fi
k get secret db-credentials
k apply --server-side=false -f workshop-k8s/db-pvc.yaml
kubectl --context=minikube get storageclass
k apply --server-side=false -f workshop-k8s/db-deployment.yaml -f workshop-k8s/db-service.yaml
k rollout status deployment/db --timeout=180s
k get pvc db-data
kubectl --context=minikube get pv
k exec deployment/db -- pg_isready -U stockline -d stockline
bash workshop-k8s/verifier.sh 6
