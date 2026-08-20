Partie 1 : 

$ docker search 2048

$ docker pull quchaonet/2048

$ docker images

$ docker run -d --name exo4-2048 -p 5000:8080 quchaonet/2048

$ docker container ls 

$ docker run -d --name exo4-2048-v2 -p 5001:8080 quchaonet/2048

$ docker ps

$ docker stop exo4-2048-v2

$ docker stop exo4-2048

$ docker ps

$ docker ps -a

$ docker start exo4-2048-v2

$ docker stop exo4-2048-v2

$ docker rmi -f quchaonet/2048

$ docker images

$ docker rm exo4-2048-v2 & docker rm exo4-2048

$ docker ps -a


Partie 2 :

$ docker pull nginx

$ docker run -d -p 5002:80 --name nginx-web nginx

$ docker images 

$ docker exec -it nginx-web bash

# cd /usr/share/nginx/html

# apt upgrade

# cp index.html index.html.bak

# apt install nano

# nano index.html 

# exit 

$ docker restart nginx-web

$ docker search apache

$ docker pull httpd

$ docker run -d -p 8083:80 --name apache-web httpd

Partie 3 : 

$ docker run -d -p 5003:80 --name nginx-web3 nginx

$ docker run -d -p 5004:80 --name nginx-web4 nginx

$ docker run -d -p 5005:80 --name nginx-web5 nginx

$ docker cp C:\Users\Administrateur\OneDrive - M2I\Bureau\.repos\LAHO_2026-07-06_Admin-Cloud\05-Docker\exercice_bis\files_tp_conteneur\html5up-editorial-m2i.zip nginx-web3:/root

$ docker exec -it nginx-web3 bash

root@8ccaa5cd41c4:/# cd /root
root@8ccaa5cd41c4:~# ls
root@8ccaa5cd41c4:~# apt upgrade
root@8ccaa5cd41c4:~# apt update
root@8ccaa5cd41c4:~# apt install unzip
unzip /root/html5up-editorial-m2i.zip ./
mv html5up-editorial-m2i.zip/* /usr/share/nginx/html

