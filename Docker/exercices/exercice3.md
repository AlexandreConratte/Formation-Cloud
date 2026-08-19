$ touch exercice3.md

$ docker search nginx

$ docker pull nginx

$ docker run -d --name exo3nginx -p 8080:80 nginx

$ $ docker container ls

$ $ docker exec -it exo3nginx sh

# ls -l

# apt show nginx

# cd /usr/share/nginx/html

# ls

# cp index.html index.html.bak 

# apt install nano

# nano index.html  

<!-- <h1>Welcome to nginx!</h1>
<p>Coucou tchuletchule, bienvenue sur mon nginx!! Modif done !</p> -->

# exit

$ docker stop exo3nginx

$ docker rm exo3nginx