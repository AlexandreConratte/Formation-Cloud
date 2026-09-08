# Partie Imperative 

minikube start

minikube status

kubectl get nodes

kubectl get all

kubectl create deployment game-2048 --image=quchaonet/2048 --replicas=1

kubectl get all

kubectl expose deployment/game-2048 --type=NodePort --port=8080

minikube service game-2048 --url   #http://127.0.0.1:18080

# Partie Declarative  

kubectl delete deployment/game-2048

kubectl delete service/game-2048

kubectl get all

kubectl apply -f deployment-2048.yaml
kubectl apply -f service-2048.yaml


