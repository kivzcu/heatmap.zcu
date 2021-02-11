#!/bin/bash
#Install all dependecies of Symfony project: composer install
cat << "EOF"
 ______  ______  __    __  ______ ______  ______  ______  ______ 
/\  ___\/\  __ \/\ "-./  \/\  == /\  __ \/\  ___\/\  ___\/\  == \  
\ \ \___\ \ \/\ \ \ \-./\ \ \  _-\ \ \/\ \ \___  \ \  __\\ \  __<  
 \ \_____\ \_____\ \_\ \ \_\ \_\  \ \_____\/\_____\ \_____\ \_\ \_\
  \/_____/\/_____/\/_/  \/_/\/_/   \/_____/\/_____/\/_____/\/_/ /_/
EOF
docker ps
docker-compose exec -T php-fpm composer --working-dir=/var/www/symfony $@
