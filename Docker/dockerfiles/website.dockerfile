FROM nginx:alpine

COPY websites/ /usr/share/nginx/html

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]