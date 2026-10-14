### Étape 1 — Vérifier le cluster utilisé

Nous allons utiliser le cluster existant **`tp-k8-v2`**. Le dossier `TP_K8_v3` contient ton travail ; son nom n’a pas besoin d’être identique à celui du cluster.

Exécute :

```
kubectl config current-context
kubectl --context=tp-k8-v2 get nodes
```

**Explication :**

- `kubectl` : outil pour communiquer avec Kubernetes.
- `config current-context` : affiche le cluster sélectionné par défaut.
- `--context=tp-k8-v2` : choisit explicitement notre cluster pour cette commande.
- `get nodes` : affiche les machines du cluster et leur état.

Ces commandes consultent l’état du cluster, sans le modifier.

**Résultat attendu :** contexte `tp-k8-v2` et nœud `Ready`.

Envoie les résultats pour valider avant de préparer l’espace de travail Kubernetes du TP complet


### Créer le namespace

Un **namespace** regroupe les ressources d’une application dans le cluster. Nous utiliserons `stockline`, comme dans l’énoncé initial. Le TP v2 utilise `stockline-tp` : ses ressources resteront séparées.

```
kubectl --context=tp-k8-v2 create namespace stockline
```

- `create namespace` : crée cet espace.
- `stockline` : son nom.

Puis sélectionne ce cluster et ce namespace pour les prochaines commandes :

```
kubectl config use-context tp-k8-v2
kubectl config set-context --current --namespace=stockline
```

Cela permet ensuite d’écrire simplement `kubectl get pods` pour consulter les Pods de `stockline`.

**Vérifie :**

```
kubectl get namespace stockline
kubectl config view --minify -o jsonpath='{.contexts[0].context.namespace}'
```

Résultats attendus : **`Active`**, puis **`stockline`**.

Si la création indique `AlreadyExists`, arrête-toi et partage ce message. Sinon, envoie les résultats des vérifications.


### Étape 1, suite — Activer les extensions prévues par l’énoncé

Nous aurons besoin de deux composants :

- **Ingress** : orientera les requêtes HTTP vers le site ou l’API à l’étape 10.
- **Metrics Server** : mesurera la consommation CPU et mémoire pour l’autoscaling à l’étape 11.

Exécute une commande à la fois :

```
minikube -p tp-k8-v2 addons enable ingress
```

```
minikube -p tp-k8-v2 addons enable metrics-server
```

**Lecture des commandes :**

- `-p tp-k8-v2` : choisit le profil Minikube de notre cluster.
- `addons enable` : installe et active une extension.
- Le dernier mot indique laquelle.

Ces composants sont installés au niveau du cluster, dans leurs propres namespaces.


```
export PATH="$PATH:/c/Program Files/Kubernetes/Minikube"
```

Cette commande conserve le PATH existant (`$PATH`) et ajoute le dossier de Minikube.



### Suite de l’étape 1 — Vérifier l’image de l’API

L’énoncé demande de disposer de l’image Docker de StockLine puis de la charger dans Minikube.

Une **image Docker** contient l’application et ses dépendances. Celle construite pendant mes tests devrait encore être présente.

Exécute la commande du TP :

```
docker images stockline-api
```

**Résultat attendu :** une ligne avec `stockline-api` et le tag `1.0.0`.


**L’image est présente.** Charge-la maintenant dans le cluster :

```
minikube -p tp-k8-v2 image load stockline-api:1.0.0
```

Cette commande rend l’image disponible aux Pods de Minikube. `-p tp-k8-v2` est l’adaptation au nom de ton cluster.

Puis vérifie avec la commande du TP :

```
minikube -p tp-k8-v2 image ls | grep stockline
```

- `image ls` : liste les images disponibles dans le cluster.
- `| grep stockline` : affiche uniquement les lignes contenant `stockline`.

**Résultat attendu :** une ligne contenant `stockline-api:1.0.0`.


### Suite de l’étape 1 — Retrouver les fichiers du TP

L’énoncé utilise une variable appelée `K8S` pour désigner le dossier des fichiers fournis. Depuis ton dossier `TP_K8_v3`, exécute :

```
export K8S="../tp"
ls "$K8S/manifests"
```

- `export K8S="../tp"` : mémorise le chemin vers le dossier `tp`, situé à côté de `TP_K8_v3`.
- `$K8S` : reprend ce chemin dans une commande.
- `ls` : affiche les manifests fournis.

Les guillemets protègent les chemins contenant des espaces.

**Résultat attendu :** les fichiers allant de `00-namespace.yaml` à `50-hpa.yaml`.


### Suite de l’étape 1 — Préparer les validations

Copie le script fourni, puis crée ton fichier de réponses :

```
cp "$K8S/workshop/verifier.sh" .
chmod +x verifier.sh
touch reponses.md
```

- `cp ... .` : copie le script dans le dossier courant (`.`).
- `chmod +x` : autorise son exécution.
- `touch` : crée un fichier vide s’il n’existe pas, sans effacer un fichier existant.

Lance ensuite le contrôle prévu par le TP :

```
./verifier.sh 1
```

`./` désigne un fichier du dossier courant et `1` sélectionne les vérifications de l’étape 1.


Le nœud est `Ready` et le namespace est accessible : **le cluster répond**. Le premier contrôle peut échouer parce que Git Bash transforme le chemin `/readyz` utilisé par le script.

Réessaie ainsi :

```
MSYS_NO_PATHCONV=1 ./verifier.sh 1
```

`MSYS_NO_PATHCONV=1` désactive cette transformation **uniquement pour cette commande**. C’est une adaptation à Git Bash sous Windows.


### Étape 2 — Créer un Pod

Un **Pod** exécute un ou plusieurs conteneurs dans Kubernetes. Nous allons créer `sonde`, un petit conteneur BusyBox qui servira à tester le réseau.

Commençons par **générer son manifest**, sans créer le Pod :

```
kubectl run sonde --image=busybox:1.36 --dry-run=client -o yaml -- sleep 36000 > pod-sonde.yaml
```

C’est la commande de l’énoncé :
c
- `run sonde` : prépare un Pod nommé `sonde`.
- `--image=busybox:1.36` : choisit son image.
- `--dry-run=client` : prépare la configuration sans l’envoyer au cluster.
- `-o yaml` : produit du YAML.
- `-- sleep 36000` : le conteneur attendra 10 heures pour rester disponible.
- `> pod-sonde.yaml` : écrit le résultat dans ce fichier.


**Le manifest est correct.** Voici les éléments principaux :

- `kind: Pod` : l’objet à créer.
- `name: sonde` : son nom.
- `labels` : une étiquette permettant de le retrouver.
- `containers` : le conteneur BusyBox et sa commande `sleep 36000`.
- `restartPolicy: Always` : Kubernetes redémarre le **conteneur** s’il s’arrête. Cela ne recrée pas un Pod supprimé.

Les champs vides comme `resources: {}` sont normaux dans ce YAML généré.

### Créer le Pod et vérifier son démarrage

Exécute les trois commandes du TP :

```
kubectl apply -f pod-sonde.yaml
kubectl wait --for=condition=Ready pod/sonde --timeout=120s
kubectl get pod sonde -o wide
```

- `apply -f` : crée le Pod décrit dans le fichier.
- `wait` : attend qu’il soit prêt, pendant 120 secondes maximum.
- `get ... -o wide` : affiche son état, son IP et son nœud.

**Résultat attendu :** `1/1` dans `READY` et `Running` dans `STATUS`.


```
kubectl describe pod sonde
```

Affiche les détails du Pod. En bas, la section **Events** retrace son démarrage : téléchargement de l’image, création et lancement du conteneur.

```
kubectl logs sonde
```

Affiche les messages du conteneur. **Une sortie vide est normale** : `sleep` n’écrit rien.

```
kubectl exec sonde -- hostname
```

Exécute `hostname` **dans le conteneur**. Résultat attendu : `sonde`. Le `--` sépare les options Kubernetes de la commande exécutée dans le conteneur.

```
kubectl exec sonde -- nslookup kubernetes.default.svc.cluster.local
```

Teste le DNS interne : ce nom désigne le Service de l’API Kubernetes. Une adresse IP doit être renvoyée :  
- `10.96.0.10` : le serveur DNS interrogé.
- `10.96.0.1` : l’adresse du Service Kubernetes trouvé.


### Suite de l’étape 2 — Supprimer le Pod et observer

Le but est de constater qu’un **Pod créé seul n’est pas recréé automatiquement** après sa suppression.

Exécute les commandes du TP :

```
kubectl delete pod sonde
kubectl get pods
```

**Résultat attendu :** `sonde` a disparu. Si aucun autre Pod n’existe dans `stockline`, tu verras `No resources found`.

Recrée-le ensuite depuis ton fichier :

```
kubectl apply -f pod-sonde.yaml
kubectl wait --for=condition=Ready pod/sonde --timeout=120s
```

Puis lance la validation, avec l’adaptation Git Bash déjà utilisée :

```
MSYS_NO_PATHCONV=1 ./verifier.sh 2
```



### Étape 3 — Le Deployment

Un **Deployment** indique à Kubernetes combien de copies de l’application doivent tourner. Il crée un **ReplicaSet**, qui maintient ce nombre de Pods, y compris lorsqu’un Pod disparaît.

Nous allons demander **deux Pods nginx** pour le site web.

Génère le manifest avec la commande du TP :

```
kubectl create deployment front --image=nginx:1.27-alpine --replicas=2 \
  --dry-run=client -o yaml > front-deployment.yaml
```

- `create deployment front` : prépare un Deployment nommé `front`.
- `--replicas=2` : demande deux Pods.
- `--dry-run=client -o yaml` : génère le YAML sans créer l’objet.
- `\` : prolonge la commande sur la ligne suivante.

Puis lis le fichier :

```
cat front-deployment.yaml
```

&#32;Le lien important est `app: front` :

- `selector.matchLabels` : le Deployment recherche les Pods portant cette étiquette.
- `template.metadata.labels` : les Pods créés recevront cette étiquette.
- `replicas: 2` : Kubernetes devra en maintenir deux.
- `template.spec.containers` : chaque Pod exécutera nginx.

Le fichier complet doit aussi contenir son début : `apiVersion`, `kind: Deployment` et `metadata`.


### Appliquer et observer

Exécute les commandes du TP :

```
kubectl apply -f front-deployment.yaml
kubectl rollout status deploy/front
kubectl get deploy,rs,pods -l app=front --show-labels
```

- `rollout status` : attend la fin du déploiement.
- `deploy,rs,pods` : affiche le Deployment, le ReplicaSet et les Pods.
- `-l app=front` : sélectionne les objets portant cette étiquette.
- `--show-labels` : affiche leurs étiquettes.

**Résultat attendu :** un Deployment prêt à `2/2`, un ReplicaSet et deux Pods `Running`.

**Les deux Pods nginx sont prêts.** Vérifions maintenant leur recréation automatique.

Exécute la commande du TP :

```
kubectl delete $(kubectl get pods -l app=front -o name | head -1) --wait=false
```

Elle se lit de l’intérieur vers l’extérieur :

- `kubectl get pods -l app=front -o name` : liste les noms des Pods du front.
- `head -1` : prend le premier.
- `$(...)` : insère ce nom dans la commande `delete`.
- `--wait=false` : rend la main sans attendre la fin de la suppression.

Observe ensuite :

```
kubectl get pods -l app=front
```

**Résultat attendu :** un nouveau Pod apparaît. Tu peux brièvement voir l’ancien en `Terminating` et le nouveau en `ContainerCreating`. Le ReplicaSet rétablit les deux Pods demandés.



### Suite de l’étape 3 — Commande ponctuelle et fichier YAML

Passe temporairement à trois Pods :

```
kubectl scale deploy/front --replicas=3
kubectl get deploy front
```

`scale` modifie le nombre de répliques dans le cluster, mais **ne modifie pas ton fichier YAML**.

Réapplique ensuite ton fichier :

```
kubectl apply -f front-deployment.yaml
kubectl get deploy front
```

Puisque le fichier contient toujours `replicas: 2`, Kubernetes revient à deux Pods. Si l’affichage est encore en transition, relance la commande `get`.

Termine avec la validation :

```
MSYS_NO_PATHCONV=1 ./verifier.sh 3
```

### Étape 4 — Donner une adresse stable au front

Les Pods peuvent être remplacés et changer d’IP. Un **Service** leur donne un point d’accès stable, ici nommé `front`. Il retrouve les Pods grâce à leur étiquette `app: front`.

Génère le manifest avec la commande du TP :

```
kubectl expose deployment front --port=80 --target-port=80 \
  --dry-run=client -o yaml > front-service.yaml
```

- `expose deployment front` : prépare un Service à partir du Deployment.
- `--port=80` : port d’entrée du Service.
- `--target-port=80` : port où nginx écoute dans les Pods.
- `--dry-run=client -o yaml` : génère le fichier sans créer le Service.

Affiche ensuite le fichier :

```
cat front-service.yaml
```


**Le manifest est correct.**

- `selector: app: front` : le Service sélectionne tes Pods nginx.
- `port: 80` : le Service reçoit les connexions sur le port 80.
- `targetPort: 80` : il les transmet au port 80 des Pods.
- Sans `type` explicite, le Service sera de type **ClusterIP**, accessible à l’intérieur du cluster.

### Créer le Service et observer ses destinations

Exécute les commandes du TP :

```
kubectl apply -f front-service.yaml
kubectl get svc front
```

`svc` est l’abréviation de `service`. Une adresse `CLUSTER-IP` doit apparaître.

Puis compare :

```
kubectl get endpointslices -l kubernetes.io/service-name=front
kubectl get pods -l app=front -o wide
```

Un **EndpointSlice** répertorie les adresses des Pods vers lesquels le Service peut envoyer le trafic.

**Résultat attendu :** les deux adresses dans `ENDPOINTS` correspondent aux IP de tes deux Pods nginx ( 10.244.0.13,10.244.0.15)

**Le Service trouve bien les deux Pods.** Testons maintenant son accès depuis `sonde`, à l’intérieur du cluster.

Exécute les commandes du TP :

```
kubectl exec sonde -- wget -qO- http://front | head -4
```

- `wget -qO-` : récupère la page et affiche son contenu dans le terminal.
- `http://front` : utilise le nom du Service.
- `head -4` : affiche seulement les quatre premières lignes.

**Résultat attendu :** le début de la page HTML nginx.

Puis teste le DNS :

```
kubectl exec sonde -- nslookup front.stockline.svc.cluster.local
```

Ce nom se décompose ainsi : Service **`front`**, namespace **`stockline`**, domaine interne **`svc.cluster.local`**.

**Résultat attendu :** l’adresse renvoyée correspond à la `CLUSTER-IP` du Service, et non à l’IP d’un Pod.

Address: 10.101.4.63 = DNS


### Accéder au front depuis ton navigateur

Le Service est interne au cluster. La commande du TP crée un accès temporaire depuis ton poste :

```
kubectl port-forward svc/front 8081:80
```

- `svc/front` : le Service à joindre.
- `8081:80` : relie le port **8081 de ton poste** au port **80 du Service**.

**Laisse cette commande tourner**, puis ouvre :

**http://localhost:8081**

Tu dois voir **« Welcome to nginx\! »**. Ensuite, reviens au terminal et fais **Ctrl+C** pour arrêter cet accès temporaire.

Lance enfin :

```
MSYS_NO_PATHCONV=1 ./verifier.sh 4
```


### Étape 5 — Remplacer la page nginx par StockLine

Nous allons utiliser un **ConfigMap** pour stocker le fichier HTML du site. Ensuite, nous le rendrons accessible dans le conteneur nginx.

Commençons par lire le début du manifest fourni, comme dans le TP :

```
head -20 "$K8S/manifests/29-front-configmap.yaml"
```

- `head -20` : affiche les vingt premières lignes.
- `$K8S` : reprend le chemin vers les fichiers fournis.

Repère ces éléments :

- `kind: ConfigMap` : le type d’objet.
- `name: front-html` : son nom.
- `data` puis `index.html: |` : le contenu du fichier HTML. Le `|` permet d’écrire du texte sur plusieurs lignes.


Crée maintenant le ConfigMap avec les commandes du TP :

```
kubectl apply -f "$K8S/manifests/29-front-configmap.yaml"
kubectl get configmap front-html
```

- `apply -f` : enregistre le ConfigMap décrit dans le fichier.
- `get configmap` : vérifie qu’il existe.

**Résultat attendu :** `front-html` apparaît avec `DATA` égal à **1**, correspondant à la clé `index.html`.

La page nginx ne change pas encore : il faudra ensuite modifier le Deployment pour qu’il utilise ce fichier.


**Le ConfigMap est créé.** Il contient notre fichier `index.html`.

### Relier ce fichier à nginx

Ouvre ton Deployment :

```
notepad front-deployment.yaml
```

Dans **`spec → template → spec`**, remplace la partie contenant `containers` par ceci. Attention : il s’agit du `spec` **dans `template`**, pas du premier `spec` du fichier.

```
    spec:
      containers:
      - image: nginx:1.27-alpine
        name: nginx
        volumeMounts:
        - name: html
          mountPath: /usr/share/nginx/html
          readOnly: true
      volumes:
      - name: html
        configMap:
          name: front-html
```

**Ce que nous ajoutons :**

- `volumes` : crée un volume nommé `html` à partir du ConfigMap `front-html`.
- `volumeMounts` : rend ce volume accessible dans le conteneur.
- `mountPath` : emplacement où nginx cherche les fichiers du site.
- `readOnly: true` : le conteneur peut lire ces fichiers, sans les modifier.