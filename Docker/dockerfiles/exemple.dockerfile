FROM alpine:latest  

LABEL org.opencontainers.image.title="DEMO Alpine Docker"
LABEL org.opencontainers.image.title="image alpine perso avec git et nano"

RUN apk update,git,nano

CMD ["sleep";"infinity"]

# docker build -t mon-image .

# docker run -d mon-imagee