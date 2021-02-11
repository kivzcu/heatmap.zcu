# DEV ONLY DOCKERFILE
FROM php:7.4-fpm-alpine
RUN apk update; \
    apk upgrade; \
    apk add --no-cache $PHPIZE_DEPS; \
    pecl install xdebug-2.9.5; \
    docker-php-ext-enable xdebug; \
    apk add autoconf openssl-dev g++ make && \
    pecl install mongodb && \
    docker-php-ext-enable mongodb; \
    apk del --purge autoconf openssl-dev g++ make;
RUN apk add npm; \
    npm install --global webpack webpack-cli;
RUN echo "**** install PHP Composer ****\n" && \
    curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/bin --filename=composer
RUN rm -rf /usr/local/etc/php/conf.d/docker-php-ext-igbinary.ini;
RUN rm -fr /usr/local/etc/php/conf.d/docker-php-ext-sodium.ini;
RUN { \
    echo '[xdebug]'; \
    echo "zend_extension=$(find /usr/local/lib/php/extensions/ -name xdebug.so)"; \
    echo 'xdebug.remote_enable = 1'; \
    echo 'xdebug.remote_port = 9001'; \
    echo 'xdebug.remote_autostart = 1'; \
    echo 'xdebug.remote_connect_back = 0'; \
    echo 'xdebug.remote_host = localhost'; \
    echo 'xdebug.idekey = VSCODE'; \
    echo 'xdebug.remote_log=/var/www/symfony/xdebug/xdebug.log'; \
    } > /usr/local/etc/php/conf.d/php-config.ini
