FROM php:7.4-fpm-alpine
RUN apk update; \
	apk upgrade; \
	apk add autoconf openssl-dev g++ make && \
    echo "**** install MongoDB ****\n" && \
	pecl install mongodb && \
	docker-php-ext-enable mongodb; \
	apk del --purge autoconf openssl-dev g++ make;
RUN apk add npm; \
    npm install --global webpack webpack-cli;
RUN echo "**** install PHP Composer ****\n" && \
    curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/bin --filename=composer