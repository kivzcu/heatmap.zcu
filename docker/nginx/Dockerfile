FROM nginx:alpine
COPY nginx.conf /etc/nginx
COPY conf.d /etc/nginx/conf.d
RUN apk add netcat-openbsd bc curl bash wget openssl; \
    apk add libressl; \
    wget -O -  https://get.acme.sh | sh; \
    cd /root/.acme.sh && bash acme.sh  --upgrade  -b  dev;
WORKDIR /var/www/
CMD ["nginx"]
