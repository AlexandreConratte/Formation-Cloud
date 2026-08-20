Etape 1 : 

$ docker volume create static-site

$ docker ps

$ docker pull nginx

$ docker run -d --name Nginx_exo5 -v static-site:/usr/share/nginx/html -p 8081:80 nginx

docker cp "C:\Users\Administrateur\OneDrive - M2I\Bureau\html5up-paradigm-shift\index.html" Nginx_exo5:/usr/share/nginx/html

$ docker exec -it Nginx_exo5 bash

root@079f79e7d482:/# cd /usr/share/nginx/html

root@079f79e7d482:/usr/share/nginx/html# ls

root@079f79e7d482:/usr/share/nginx/html/html5up-paradigm-shift# mv * /usr/share/nginx/html/

root@079f79e7d482:/usr/share/nginx/html# exit

$ docker stop Nginx_exo5

$ docker rm Nginx_exo5

Etape 2 : 

$ docker pull httpd

$ docker ps

$ docker run -d --name apache_exo5 -v static-site:/usr/share/httpd/html -p 8081:80 httpd

$ docker stop apache_exo5

$ docker rm apache_exo5

$ docker volume ls

Etape 3 : 

$ docker search caddy

$ docker pull caddy

$ docker run -d --name caddy_exo5 -v static-site:/usr/share/caddy -p 8082:80 caddy