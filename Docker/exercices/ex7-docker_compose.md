touch compose.yml 

Compose.yml : 
services:
    site1:
      image: nginx:alpine
      container_name: html5up-site1
      ports:
        - "8081:80"
      volumes:
        - ./sites/site1:/usr/share/nginx/html:ro
      restart: unless-stopped

    site2:
      image: nginx:alpine
      container_name: html5up-site2
      ports:
        - "8082:80"
      volumes:
        - ./sites/site2:/usr/share/nginx/html:ro
      restart: unless-stopped

    site3:
      image: nginx:alpine
      container_name: html5up-site3
      ports:
        - "8083:80"
      volumes:
        - ./sites/site3:/usr/share/nginx/html:ro
      restart: unless-stopped


docker compose up -d

docker compose ps

docker compose down