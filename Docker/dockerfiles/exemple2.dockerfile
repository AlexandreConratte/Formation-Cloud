FROM nginx

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*

#RUN rm -rf /usr/share/nginx/html/*

COPY ./index.html /usr/share/nginx/html

#port
EXPOSE 80 

# nginx -g daemon off

CMD ["nginx","-g","daemon off;"]

# docker build -t site-perso:v1

# docker run -p 80:80 --name site site-perso:v1

