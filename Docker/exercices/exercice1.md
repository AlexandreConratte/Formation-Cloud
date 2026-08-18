docker search alpine

docker pull alpine 

docker run -it --name exo-alpine-git alpine

/ # apk update

/ # apk add git

/ # git --version

/ # git --version

/ # git clone https://github.com/AlexandreConratte/Formation-Cloud.git

/ # ls

/ # cd Formation-Cloud

/Formation-Cloud # exit

docker exec -it exo-alpine-git sh

/ # cd Formation-Cloud

/Formation-Cloud # apk add nano

/Formation-Cloud # nano README.md


  GNU nano 9.2                                                                            README.md                                                                                       
# Formation-CloudCoucou c'est tchoutchou


$ docker cp exo-alpine-git:/Formation-Cloud/README.md ./
Successfully copied 26B (transferred 2.05kB) to C:\Users\Administrateur\OneDrive - M2I\Bureau\.repos\Formation-Cloud\Docker\exercices\.\