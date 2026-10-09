
**Partie 1 — Politique A : S3 avec un préfixe interdit**


*1-Un membre du groupe télécharge (s3:GetObject) le fichier rapports/ventes-2026.csv du bucket formation-documents. Autorisé ou refusé ?*


Refusé car le deny de s3:GetObject" sur la resource  "arn:aws:s3:::formation-documents/confidentiel/*" (donc formation-documents) prend le dessus 



*2-Le même membre télécharge confidentiel/salaires.xlsx. Autorisé ou refusé ? Quel statement s'applique en dernier ressort ?*


Refusé, car le statement Deny explicite appliqué sur "arn:aws:s3:::formation-documents/confidentiel/*" prend le dessus sur les autres autorisations.


*3-Il tente de supprimer (s3:DeleteObject) le fichier rapports/ventes-2026.csv. Autorisé ou refusé ? S'agit-il d'un deny explicite ou d'un deny implicite ?*

Refusé, il s'agit d'un deny implicite car il n'avait l'autorisation que du s3:get et s3:list, le reste est donc en deny implicites


*4-Il liste le contenu du bucket (s3:ListBucket). Peut-il voir dans la liste que le dossier confidentiel/ existe et les noms des fichiers qu'il contient ?*

Autorisé car il peut list le dossier confidentiel présent dans la liste, mais pas ce qu'il contient (get)


*5-Un administrateur ajoute plus tard au groupe une politique AmazonS3FullAccess (gérée AWS, qui autorise s3:* sur *). Le téléchargement de confidentiel/salaires.xlsx devient-il possible ? Pourquoi ?*


Refusé, car le "Sid": "InterdireConfidentiel" : Deny sur confidentiel/salaires annule les quelconques autorisations Allow existantes sur ce dossier





**Partie 2 — Politique B : EC2 sous conditions**

*1-stagiaire-ops lance une instance t3.micro dans eu-west-3. Autorisé ou refusé ?*

Autorisé, car la condition "aws:RequestedRegion": "eu-west-3" est validé



*2-Il lance une instance t3.micro dans eu-central-1 (Francfort). Autorisé ou refusé ? Est-ce un deny explicite ?*

Refusé,  "aws:RequestedRegion": "eu-west-3" l'en empéchant 


*3-Il lance une instance m5.large dans eu-west-3. Autorisé ou refusé ?*

Refusé, car instance de type m5.large et non t3.micro


*4-Il exécute aws ec2 describe-instances --region us-east-1. Autorisé ou refusé ?*

Autorisé, l'action Describe étant Allow sur * (tout)


*5-Il tente d'arrêter (ec2:StopInstances) une instance existante à Paris. Autorisé ou refusé ?*


Refusé par deny implicite, n'ayant pas eu la policy Allow pour cette action


*6-Les deux clés de la Condition (aws:RequestedRegion et ec2:InstanceType) sont dans le même bloc StringEquals. L'instance doit-elle satisfaire les deux conditions, ou une seule suffit-elle ?*

Elle doit satisfaire les deux instances ensemble car sinon cela autoriserait les instances t3.micro dans les autres régions, ou les instances autres que t3.micro dans la région eu-west-3, ce qui n'est pas le but recherché par cette policy.


**Partie 3 — Politique gérée ReadOnlyAccess vs politique inline**

*1-L'auditeur (avec ReadOnlyAccess) peut-il lister les utilisateurs IAM du compte ? Peut-il en créer un ?*

Oui, il peut lister car il a l'action im:List Allow , par contre il n'a pas d'action iam:create parmis les actions autorisées donc ne peut pas en créer un


*2-L'auditeur peut-il télécharger un objet S3 ? Peut-il en téléverser (s3:PutObject) un ?*

Il peut télécharger un objet s3 ( car allow : "s3:Get*") mais pas le téleverser (pas présent dans la liste Action)


*3-Citez deux avantages concrets d'une politique gérée (AWS ou client) par rapport à une politique inline.*

La politique inline est appliquée à un seul individu, et peut être longue à réaliser (selon le nombre d'action) alors que la politique gérée est réutilisable et appliquable plus facilement


*4-La politique inline de dupont autorise s3:* sur les objets du bucket. Peut-il pour autant supprimer le bucket lui-même (s3:DeleteBucket) ? Regardez bien le Resource.*


Il ne peut supprimer le bucket lui-même, uniquement ce qu'il y a dedans car la ressource est formation-documents/* (/* est à retenir)


*5-En audit, pourquoi les politiques inline sont-elles plus difficiles à repérer que les politiques gérées ? Quel risque le Sid de celle-ci révèle-t-il sur les pratiques de l'équipe ?*

Les politiques inline sont plus difficiles à repérer car il faudrait les repérer au cas par cas, en vérifiant chaque utiliser/iam directement

Le sid annonce que l'utilisateur a été crée d'urgence pour un dépannage, et pourtant il est encore existant et n'a donc pas été supprimé.








