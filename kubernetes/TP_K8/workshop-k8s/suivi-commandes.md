# Suivi du TP Kubernetes avec Git Bash

Date : 29 septembre 2026 — étapes 1 à 7 validées.

Les étapes 1 à 4 ont été exécutées depuis PowerShell : leurs commandes sont traduites ici en Bash pour pouvoir les reproduire. Les étapes 5 à 7 ont été exécutées avec Git Bash. Toutes les commandes présentées dans ce guide s’utilisent dans Git Bash. Elles sont regroupées et simplifiées pour l’apprentissage.

**Arrêt demandé après l’étape 7.** L’étape 8 n’a pas été exécutée. Le cluster et les applications sont laissés dans leur état actuel ; aucune commande d’arrêt ou de suppression n’a été lancée à cette occasion.

**Les ressources existent déjà. Ne rejouez pas tout le document sur le cluster actuel.** Les créations sont présentées pour comprendre le parcours et le reproduire dans un environnement neuf. Chaque nouvelle étape du TP sera expliquée et soumise à confirmation.

## 1. Ouvrir Git Bash et se placer dans TP_K8

Dans l’Explorateur Windows, ouvrir `TP_K8`, puis utiliser « Open Git Bash here » (éventuellement dans « Afficher plus d’options »). Autre possibilité, dans Git Bash :

```bash
cd '/c/Users/Administrateur/OneDrive - M2I/Bureau/.repos/Formation-Cloud/TP_K8'
pwd
ls -la
export PATH="$PWD/outils:$PATH"
export MSYS_NO_PATHCONV=1
```

- `cd` change de dossier ; les guillemets protègent les espaces du chemin.
- `pwd` affiche le dossier courant ; `ls -la` liste son contenu, fichiers cachés compris.
- Dans Git Bash, le disque `C:` s’écrit `/c/`.
- L’ajout au `PATH` permet d’écrire `minikube` au lieu de `./outils/minikube.exe`.
- `MSYS_NO_PATHCONV=1` empêche Git Bash de transformer des arguments tels que `/readyz` ou `/usr/share/nginx/html` en chemins Windows lors des appels à `kubectl.exe`.

Ces deux variables ne modifient pas la configuration permanente : les rétablir à l’ouverture d’un nouveau terminal. Toutes les commandes du guide supposent que vous restez à la racine **TP_K8**.

### Quelques repères Bash

| Syntaxe | Signification |
|---|---|
| `cat fichier` | Lire un fichier. |
| `head -20 fichier` | Afficher ses 20 premières lignes. |
| `mkdir -p dossier` | Créer un dossier s’il manque. |
| `cp source destination` | Copier un fichier ; `cp -r` pour un dossier. |
| `commande > fichier` | Écrire la sortie dans un fichier en remplaçant son contenu. |
| `commande1 \| commande2` | Transmettre la sortie de la première à la seconde. |
| `grep texte` | Garder les lignes contenant un texte. |
| `$(commande)` | Récupérer la sortie d’une commande. |
| `\` en fin de ligne | Continuer la commande à la ligne suivante. |
| `Ctrl+C` | Arrêter la commande au premier plan. |

Git Bash est le terminal utilisé ici ; aucune commande Git de commit ou de publication n’a été nécessaire.

## 2. Lire les fichiers et vérifier les outils

```bash
cat workshop-revision-kubernetes.md
cat stockline/README.md
cat stockline-docker/README.md
command -v docker kubectl minikube helm bash
docker version
kubectl version --client
kubectl config current-context
kubectl config get-contexts
wsl.exe --list --verbose
```

`command -v` cherche les exécutables. `docker version` contrôle aussi la connexion au moteur Docker. Les commandes `config` indiquent quel cluster kubectl cible. WSL a été consulté pour connaître l’environnement Windows disponible.

Au départ : Docker Desktop opérationnel en mode Linux, kubectl et Bash présents, Minikube et Helm absents du PATH, aucun contexte Kubernetes configuré. Helm reste à installer pour l’étape 13.

## 3. Installer Minikube — déjà fait

Voici l’équivalent Bash du téléchargement et de la vérification, fixé sur la version installée pendant ce TP :

```bash
mkdir -p outils
base='https://github.com/kubernetes/minikube/releases/download/v1.39.0'
curl -fL "$base/minikube-windows-amd64.exe" -o outils/minikube.exe
curl -fL "$base/minikube-windows-amd64.exe.sha256" -o outils/minikube.exe.sha256
expected=$(awk '{print $1}' outils/minikube.exe.sha256 | tr -d '\r\n')
printf '%s  outils/minikube.exe\n' "$expected" | sha256sum -c -
# Continuer uniquement si la vérification affiche OK.
./outils/minikube.exe version
```

`curl -fL` télécharge en suivant les redirections et signale les erreurs HTTP. SHA-256 compare le fichier reçu à l’empreinte publiée. **Résultat obtenu : v1.39.0, empreinte validée.**

Source : [installation officielle Minikube](https://minikube.sigs.k8s.io/docs/start/).

## 4. Démarrer le cluster

```bash
minikube start --driver=docker --cpus=2 --memory=3072
minikube status
kubectl config current-context
kubectl --context=minikube get nodes
kubectl --context=minikube get pods -A
```

Minikube crée le nœud dans Docker avec une demande de 2 processeurs et 3 072 Mio de mémoire. `get nodes` vérifie qu’il est `Ready`. `-A` affiche les pods de tous les namespaces.

**Résultat : Kubernetes v1.37.0, nœud prêt et composants système démarrés.** `--context=minikube` cible explicitement le bon cluster.

## 5. Activer les extensions

```bash
minikube addons enable ingress
minikube addons enable metrics-server
kubectl --context=minikube -n ingress-nginx rollout status deployment/ingress-nginx-controller --timeout=45s
kubectl --context=minikube -n kube-system rollout status deployment/metrics-server --timeout=45s
kubectl --context=minikube get apiservice v1beta1.metrics.k8s.io
kubectl --context=minikube top nodes
```

Ingress permettra le routage HTTP. Metrics Server fournit les mesures CPU/mémoire nécessaires à l’autoscaling. `rollout status` attend que le Deployment soit disponible ; `top nodes` affiche les mesures.

Le premier contrôle de Metrics Server a expiré. Pour comprendre :

```bash
kubectl --context=minikube -n kube-system logs deployment/metrics-server --tail=40
```

Il attendait ses premières métriques. **Les deux extensions sont devenues disponibles sans correction.**

## 6. Préparer l’image StockLine

```bash
cat stockline-docker/Dockerfile
cat stockline-docker/.dockerignore
cat stockline/requirements.txt
docker image ls stockline-api:1.0.0
# Copies réalisées lorsque les destinations étaient absentes :
cp -r stockline/app stockline-docker/app
cp stockline/requirements.txt stockline-docker/requirements.txt
docker build -t stockline-api:1.0.0 ./stockline-docker
minikube -p minikube image load stockline-api:1.0.0
minikube -p minikube image ls | grep stockline-api
```

Le contexte `stockline-docker` doit contenir le code et les dépendances. `build -t` construit l’image et lui donne son nom/version. `image load` la transfère dans Minikube : la présence d’une image dans Docker Desktop ne suffit pas à la rendre disponible au moteur du cluster.

**Résultat : `stockline-api:1.0.0` construite et chargée. L’API n’est pas encore déployée.**

## 7. Dossier de travail et namespace — étape 1

```bash
mkdir -p workshop-k8s
cp workshop/verifier.sh workshop-k8s/verifier.sh
touch workshop-k8s/reponses.md
kubectl --context=minikube get namespace stockline --ignore-not-found
# À créer seulement s’il est absent :
kubectl --context=minikube create namespace stockline
kubectl config set-context minikube --namespace=stockline
kubectl config current-context
bash workshop-k8s/verifier.sh 1
```

Le namespace regroupe les ressources de StockLine. `set-context` en fait le namespace par défaut de Minikube. `touch` crée le fichier de réponses s’il manque. Lancer le script avec `bash` évite de dépendre du droit d’exécution Windows.

**Résultat : 4 contrôles OK.** `reponses.md` reste à remplir.

## 8. Le Pod — étape 2

### Générer, créer et inspecter

```bash
kubectl --context=minikube -n stockline run sonde --image=busybox:1.36 \
  --dry-run=client -o yaml -- sleep 36000 > workshop-k8s/pod-sonde.yaml
cat workshop-k8s/pod-sonde.yaml
kubectl --context=minikube apply --server-side=false -f workshop-k8s/pod-sonde.yaml
kubectl --context=minikube -n stockline wait --for=condition=Ready pod/sonde --timeout=45s
kubectl --context=minikube -n stockline get pod sonde -o wide
kubectl --context=minikube -n stockline describe pod sonde
kubectl --context=minikube -n stockline logs sonde
kubectl --context=minikube -n stockline exec sonde -- hostname
kubectl --context=minikube -n stockline exec sonde -- nslookup kubernetes.default.svc.cluster.local
```

- `--dry-run=client -o yaml` génère le fichier sans créer la ressource.
- `apply -f` applique ce fichier. `--server-side=false` conserve le fonctionnement côté client et l’annotation attendue par le vérificateur du TP.
- `sleep 36000` garde le conteneur actif pendant 10 heures.
- `describe` montre notamment les événements ; `logs` est vide ici, car `sleep` n’écrit rien.
- `exec` lance une commande dans le conteneur ; `nslookup` teste le DNS.

### Supprimer et recréer

```bash
kubectl --context=minikube -n stockline delete pod sonde --timeout=45s
kubectl --context=minikube -n stockline get pods
kubectl --context=minikube apply --server-side=false -f workshop-k8s/pod-sonde.yaml
kubectl --context=minikube -n stockline wait --for=condition=Ready pod/sonde --timeout=45s
bash workshop-k8s/verifier.sh 2
```

Sans contrôleur, le pod supprimé ne revient pas. `restartPolicy: Always` redémarre ses conteneurs si nécessaire, mais ne recrée pas le pod supprimé. `READY 1/1` indique un conteneur prêt sur un ; `RESTARTS 0` indique aucun redémarrage.

**Résultat : 4 contrôles OK après recréation.**

## 9. Le Deployment — étape 3

```bash
kubectl --context=minikube -n stockline create deployment front \
  --image=nginx:1.27-alpine --replicas=2 --dry-run=client -o yaml \
  > workshop-k8s/front-deployment.yaml
cat workshop-k8s/front-deployment.yaml
kubectl --context=minikube apply --server-side=false -f workshop-k8s/front-deployment.yaml
kubectl --context=minikube -n stockline rollout status deployment/front --timeout=45s
kubectl --context=minikube -n stockline get deployment,replicaset,pods -l app=front --show-labels
```

Le Deployment crée un ReplicaSet qui maintient deux pods. `-l app=front` filtre les ressources par label. **Ne régénérez pas ce fichier maintenant : il contient depuis l’étape 5 le montage du ConfigMap.**

```bash
pod=$(kubectl --context=minikube -n stockline get pods -l app=front -o name | head -1)
kubectl --context=minikube -n stockline delete "$pod" --timeout=45s
kubectl --context=minikube -n stockline rollout status deployment/front --timeout=45s
kubectl --context=minikube -n stockline get pods -l app=front
kubectl --context=minikube -n stockline scale deployment/front --replicas=3
kubectl --context=minikube -n stockline rollout status deployment/front --timeout=45s
kubectl --context=minikube -n stockline get deployment front
kubectl --context=minikube apply --server-side=false -f workshop-k8s/front-deployment.yaml
kubectl --context=minikube -n stockline rollout status deployment/front --timeout=45s
bash workshop-k8s/verifier.sh 3
```

Le ReplicaSet remplace le pod supprimé. Le passage manuel à trois replicas atteint `3/3`, puis le fichier réappliqué rétablit les deux replicas qu’il décrit. Pour conserver une modification, il faut aussi la reporter dans le manifeste.

**Résultat : 4 contrôles OK, retour à 2/2.**

## 10. Le Service et le DNS — étape 4

```bash
kubectl --context=minikube -n stockline expose deployment front \
  --port=80 --target-port=80 --dry-run=client -o yaml > workshop-k8s/front-service.yaml
cat workshop-k8s/front-service.yaml
kubectl --context=minikube apply --server-side=false -f workshop-k8s/front-service.yaml
kubectl --context=minikube -n stockline get svc front
kubectl --context=minikube -n stockline get endpointslices -l kubernetes.io/service-name=front
kubectl --context=minikube -n stockline get pods -l app=front -o wide
kubectl --context=minikube -n stockline exec sonde -- wget -qO- -T 5 http://front
kubectl --context=minikube -n stockline exec sonde -- nslookup front.stockline.svc.cluster.local
```

Le Service fournit un nom DNS et une IP stables. Son sélecteur `app: front` choisit les pods. `port` désigne le port du Service et `targetPort` celui du conteneur. Les EndpointSlices contiennent les IP des pods sélectionnés ; le DNS renvoie la ClusterIP du Service.

### Accès temporaire depuis le poste

Premier terminal Git Bash :

```bash
kubectl --context=minikube -n stockline port-forward svc/front 8081:80 --address=127.0.0.1
```

Deuxième terminal :

```bash
curl -i http://127.0.0.1:8081
```

On peut aussi ouvrir cette adresse dans le navigateur. Arrêter le premier terminal avec `Ctrl+C` après le test. Le port-forward donne un accès temporaire à un pod choisi par le Service, sans publication sur Internet.

```bash
bash workshop-k8s/verifier.sh 4
```

**Résultat : HTTP 200, DNS correct, deux endpoints et 3 contrôles OK. Le port-forward de notre test est arrêté.**

## 11. Le ConfigMap monté en fichier — étape 5

Le manifeste mentionné dans le TP était absent. Nous avons donc préparé une copie de la page Docker puis généré le ConfigMap. Les commandes de préparation et de déploiement réellement exécutées sont aussi conservées dans `etape-5.sh` ; ce script refuse de remplacer une page ou un manifeste déjà existant.

### Préparer la page et le ConfigMap

```bash
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
```

`sed -i` modifie la copie HTML : titre adapté à Kubernetes, description simplifiée et commentaire de routage corrigé. La source Docker reste conservée. `--from-file=index.html=...` place le contenu dans la clé `index.html` du ConfigMap. Un ConfigMap contient des données non sensibles.

### Modifier le Deployment

Dans `workshop-k8s/front-deployment.yaml`, nous avons ajouté `volumeMounts` au conteneur nginx et `volumes` au même niveau que `containers`. La section `spec.template.spec` contient maintenant :

```yaml
    spec:
      containers:
      - image: nginx:1.27-alpine
        name: nginx
        resources: {}
        volumeMounts:
        - name: html
          mountPath: /usr/share/nginx/html
          readOnly: true
      volumes:
      - name: html
        configMap:
          name: front-html
```

`volumes` définit la source ; `volumeMounts` indique où elle apparaît dans le conteneur. La clé `index.html` devient un fichier dans le répertoire servi par nginx. Le montage est en lecture seule.

### Appliquer et contrôler

```bash
kubectl --context=minikube -n stockline apply --server-side=false -f workshop-k8s/front-deployment.yaml
kubectl --context=minikube -n stockline rollout status deployment/front --timeout=45s
kubectl --context=minikube -n stockline exec deployment/front -- ls /usr/share/nginx/html
kubectl --context=minikube -n stockline exec sonde -- wget -qO- -T 5 http://front | grep '<title>'
kubectl --context=minikube -n stockline get deployment,replicaset,pods -l app=front
bash workshop-k8s/verifier.sh 5
```

Le changement du modèle des pods déclenche un nouveau ReplicaSet et leur remplacement progressif, même si l’image et le nombre de replicas restent identiques.

La première requête HTTP a expiré immédiatement après le déploiement. Nous avons relu les endpoints et l’état des pods, puis retesté avec `wget -T 10` : la page complète a été servie. La cause exacte du premier timeout n’a pas été établie ; aucune modification supplémentaire n’a été nécessaire.

**Résultat : Deployment à 2/2, titre « StockLine — Inventaire (Kubernetes) », 3 contrôles OK.** L’ancien ReplicaSet est à zéro replica. Les nouveaux endpoints sont `10.244.0.13` et `10.244.0.14` lors du contrôle.

La page est servie, mais les produits ne peuvent pas encore se charger : l’API, la base de données et le routage `/api` seront mis en place dans les étapes suivantes.

## 12. Secret, stockage persistant et PostgreSQL — étape 6

Les manifestes du support étant absents, nous avons créé `db-pvc.yaml`, `db-deployment.yaml` et `db-service.yaml` dans `workshop-k8s`. Le script exécuté est conservé dans `etape-6.sh` ; il conserve un Secret déjà existant.

### Créer les identifiants

```bash
# À exécuter uniquement si le Secret est absent :
kubectl --context=minikube -n stockline get secret db-credentials --ignore-not-found
password=$(openssl rand -hex 16)
kubectl --context=minikube -n stockline create secret generic db-credentials \
  --from-literal=POSTGRES_USER=stockline \
  --from-literal=POSTGRES_PASSWORD="$password" \
  --from-literal=POSTGRES_DB=stockline
unset password
kubectl --context=minikube -n stockline get secret db-credentials
```

`openssl rand -hex 16` produit 16 octets aléatoires représentés par 32 caractères hexadécimaux. Le mot de passe a été transmis au Secret sans être affiché ni écrit dans un fichier local. `unset` retire la variable du shell après utilisation. Le Secret contient trois clés ; son contenu n’a pas été affiché dans nos sorties.

Un Secret n’est pas chiffré simplement parce que ses valeurs apparaissent en base64 dans un YAML. Par exemple, `c3RvY2tsaW5l` se décode en `stockline` : les droits d’accès au cluster restent essentiels. Ne pas remplacer arbitrairement le Secret d’une base déjà initialisée : les variables PostgreSQL ne réinitialisent pas le mot de passe d’une base existante.

### Demander le stockage

```bash
cat workshop-k8s/db-pvc.yaml
kubectl --context=minikube -n stockline apply --server-side=false -f workshop-k8s/db-pvc.yaml
kubectl --context=minikube get storageclass
```

Le PVC `db-data` demande `1Gi` et `ReadWriteOnce`. Aucune classe n’est imposée dans le fichier : la StorageClass par défaut `standard` est utilisée. Son provisionneur `k8s.io/minikube-hostpath` crée le PV correspondant.

`ReadWriteOnce` signifie montage en lecture-écriture depuis un seul nœud, pas nécessairement par un seul pod. Nous utilisons donc également un seul replica PostgreSQL et la stratégie `Recreate` pour éviter le chevauchement de deux instances lors des mises à jour du Deployment.

### Déployer PostgreSQL et son Service

```bash
cat workshop-k8s/db-deployment.yaml
cat workshop-k8s/db-service.yaml
kubectl --context=minikube -n stockline apply --server-side=false \
  -f workshop-k8s/db-deployment.yaml -f workshop-k8s/db-service.yaml
kubectl --context=minikube -n stockline rollout status deployment/db --timeout=180s
kubectl --context=minikube -n stockline get pvc db-data
kubectl --context=minikube get pv
kubectl --context=minikube -n stockline exec deployment/db -- pg_isready -U stockline -d stockline
bash workshop-k8s/verifier.sh 6
```

Points à repérer dans le Deployment :

- `image: postgres:16` et `replicas: 1` : une instance PostgreSQL.
- `strategy.type: Recreate` : arrêt des anciens pods avant leur remplacement, avec une interruption de service pendant une mise à jour.
- `envFrom.secretRef` : injection des trois paramètres PostgreSQL depuis `db-credentials`.
- `volumeMounts` : montage de `db-data` dans `/var/lib/postgresql/data` ; les données ne sont pas limitées au système de fichiers éphémère du conteneur.
- `readinessProbe` : exécution de `pg_isready` pour indiquer quand la base accepte des connexions.
- Le Service `db` sélectionne `app: db` et fournit le port interne `5432`.

**Résultat : 5 contrôles OK.** Secret présent avec sa clé de mot de passe, PVC `Bound` de 1 Gi, un pod prêt et connexion TCP possible depuis `sonde` vers `db:5432`. `pg_isready` indique `accepting connections`. La persistance après suppression du pod sera testée à l’étape 8.

Le PV utilise la politique `Delete` : supprimer le PVC peut entraîner la suppression du stockage associé. Nous n’avons supprimé ni le PVC ni le PV.

## 13. Déployer l’API StockLine — étape 7

Nous avons créé `api-configmap.yaml`, `api-deployment.yaml` et `api-service.yaml`. Le script exécuté, avec les contrôles et les données d’essai, est conservé dans `etape-7.sh`.

### Configuration et déploiement

```bash
cat workshop-k8s/api-configmap.yaml
cat workshop-k8s/api-deployment.yaml
cat workshop-k8s/api-service.yaml
kubectl --context=minikube -n stockline apply --server-side=false \
  -f workshop-k8s/api-configmap.yaml \
  -f workshop-k8s/api-deployment.yaml \
  -f workshop-k8s/api-service.yaml
kubectl --context=minikube -n stockline rollout status deployment/api --timeout=180s
kubectl --context=minikube -n stockline get pods -l app=api
```

- Le ConfigMap `api-config` fournit `DB_HOST=db` et `DB_PORT=5432`.
- Le Deployment demande deux replicas de `stockline-api:1.0.0`. `imagePullPolicy: IfNotPresent` utilise l’image déjà chargée dans Minikube.
- `DB_USER`, `DB_PASSWORD` et `DB_NAME` proviennent du Secret `db-credentials` grâce à `secretKeyRef`.
- `DATABASE_URL` assemble les variables précédentes : `postgresql+psycopg2://$(DB_USER):$(DB_PASSWORD)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)`. Cette syntaxe est interprétée par Kubernetes dans le manifeste ; ce n’est pas une commande Bash à exécuter.
- Le Service `api` expose le port interne 80 et transmet vers le port 8000 du conteneur.

### Vérifier la santé et la configuration sans afficher le mot de passe

```bash
kubectl --context=minikube -n stockline exec sonde -- wget -qO- -T 10 http://api/sante
kubectl --context=minikube -n stockline exec deployment/api -- python -c '
import os
for key in ("DB_HOST", "DB_PORT", "DB_USER", "DB_NAME", "DB_SERVICE_HOST", "DB_SERVICE_PORT"):
    if key in os.environ:
        print(key + "=" + os.environ[key])
'
```

Réponse santé observée : `{"statut":"ok","base_de_donnees":"ok","version":"1.0.0"}`. Nous avons également vérifié `/sante` directement dans chacun des deux pods avec Python, pour confirmer que les deux instances joignent PostgreSQL.

Le premier test a rencontré un refus de connexion avant que le processus HTTP soit prêt. Le script attend désormais la réponse de chaque instance pendant une durée limitée. Sans readinessProbe, un pod peut apparaître prêt alors que l’application n’écoute pas encore ; les probes sont prévues à l’étape 11.

Les variables `DB_SERVICE_HOST` et `DB_SERVICE_PORT` ont été ajoutées automatiquement par Kubernetes pour le Service `db` existant au démarrage du pod. Nous utilisons le DNS `db`, qui permet de retrouver le Service sans figer son adresse dans la configuration applicative.

Contrairement à un affichage complet de `env`, notre sélection ne révèle ni `DB_PASSWORD` ni `DATABASE_URL`. En production, l’accès `kubectl exec` doit être limité aux personnes autorisées à accéder aux données sensibles du conteneur.

### Créer le produit et les 20 unités

Lecture préalable :

```bash
kubectl --context=minikube -n stockline exec sonde -- wget -qO- -T 10 http://api/produits
```

La liste était vide. Nous avons ensuite exécuté :

```bash
kubectl --context=minikube -n stockline exec sonde -- wget -qO- -T 10 \
  --header 'Content-Type: application/json' \
  --post-data '{"reference":"SSD-500","nom":"Disque SSD 500 Go","prix_unitaire":59.9,"seuil_alerte":5}' \
  http://api/produits
```

`--post-data` envoie une requête POST et le corps JSON. Le produit créé a reçu l’identifiant **1**. Le script récupère l’identifiant réel de la réponse, puis l’utilise pour le mouvement ; dans notre exécution cela correspond à :

```bash
kubectl --context=minikube -n stockline exec sonde -- wget -qO- -T 10 \
  --header 'Content-Type: application/json' \
  --post-data '{"produit_id":1,"type":"entree","quantite":20}' \
  http://api/mouvements
kubectl --context=minikube -n stockline exec sonde -- wget -qO- -T 10 http://api/stocks/1
bash workshop-k8s/verifier.sh 7
```

**Ne pas rejouer le POST de mouvement : chaque appel ajoute 20 unités supplémentaires.** Le script refuse de créer les données si la liste des produits n’est plus vide ; en cas de reprise partielle, lire les produits, mouvements et stocks avant toute nouvelle écriture.

**Résultat : 4 contrôles OK.** Deux pods prêts et sains, produit `SSD-500` d’identifiant 1, entrée de stock d’identifiant 1, quantité **20**, seuil **5**, `alerte: false`.

### Redémarrage initial observé

Un des deux pods a redémarré une fois. Diagnostic effectué :

```bash
# Ce nom est celui observé pendant notre exécution.
kubectl --context=minikube -n stockline logs api-667b74cbdf-b9plm --previous --tail=18
kubectl --context=minikube -n stockline get pods -l app=api
```

`--previous` consulte les journaux du conteneur précédent. Ils montrent une erreur `UniqueViolation` sur `produits_id_seq` : les deux processus ont tenté simultanément de créer les tables via `init_db()`. Après le redémarrage, les tables existaient et les deux instances ont répondu correctement. Le code applicatif n’a pas été modifié ; cette initialisation concurrente reste une limite du TP sur une base vierge. Une initialisation des tables exécutée une seule fois avant les replicas éviterait cette concurrence.

## État actuel et suite

- Étapes 1 à 7 validées.
- Cluster Minikube actif ; namespace par défaut `stockline`.
- Image de l’API chargée ; pod `sonde`, front nginx, Service `front` et ConfigMap `front-html` présents.
- PostgreSQL opérationnel : Secret `db-credentials`, PVC `db-data`, Deployment `db` et Service `db` créés.
- API opérationnelle avec deux replicas, ConfigMap `api-config` et Service `api` ; produit `SSD-500` en stock à 20 unités.
- Aucun port-forward de notre test laissé actif.
- `reponses.md` reste vide ; les explications de révision figurent dans ce guide.
- Prochaine étape : supprimer puis laisser recréer le pod PostgreSQL et vérifier que le stock reste à 20, après votre confirmation. Le PVC sera conservé.

Le fichier principal est **`suivi-commandes.md`**, entièrement en Git Bash. `suivi-commandes-bash.md` en contient une copie identique à la date de cet arrêt.
