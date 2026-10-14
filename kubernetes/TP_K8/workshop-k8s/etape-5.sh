#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export MSYS_NO_PATHCONV=1

# Préparer une copie locale de la page Docker pour Kubernetes.
if [[ -e workshop-k8s/index.html || -e workshop-k8s/front-configmap.yaml ]]; then
  echo 'La page ou le ConfigMap existe déjà : vérifier les fichiers avant de relancer.' >&2
  exit 1
fi
cp stockline-docker/front/index.html workshop-k8s/index.html
sed -i 's/Inventaire (conteneurs)/Inventaire (Kubernetes)/' workshop-k8s/index.html
sed -i '/<p class="muted">Version conteneurisée/,/sur la même origine/c\  <p class="muted">Gestion des produits et des stocks.</p>' workshop-k8s/index.html
sed -i 's@// nginx proxifie /api/ vers le service `api` du réseau Compose.@// L’Ingress acheminera /api/ vers le Service api à l’étape 10.@' workshop-k8s/index.html

kubectl --context=minikube -n stockline create configmap front-html \
  --from-file=index.html=workshop-k8s/index.html \
  --dry-run=client -o yaml > workshop-k8s/front-configmap.yaml
head -20 workshop-k8s/front-configmap.yaml
kubectl --context=minikube -n stockline apply --server-side=false -f workshop-k8s/front-configmap.yaml
kubectl --context=minikube -n stockline get configmap front-html
kubectl --context=minikube -n stockline apply --server-side=false -f workshop-k8s/front-deployment.yaml
kubectl --context=minikube -n stockline rollout status deployment/front --timeout=45s
kubectl --context=minikube -n stockline exec deployment/front -- ls /usr/share/nginx/html
kubectl --context=minikube -n stockline exec sonde -- wget -qO- -T 5 http://front | grep '<title>'
kubectl --context=minikube -n stockline get deployment,replicaset,pods -l app=front
bash workshop-k8s/verifier.sh 5
