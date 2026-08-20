FROM nginx

WORKDIR /usr/share/nginx/html


RUN apt update && apt install git -y

RUN rm -rf ./*

RUN git clone https://github.com/withaarzoo/3D-Rotate-Tube.git .



EXPOSE 80


CMD ["nginx","-g","daemon off;"]

