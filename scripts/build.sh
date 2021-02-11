#!/bin/bash
docker-compose down
docker-compose -f docker-compose.yml -f docker-compose-prod.yml up --build -d
docker-compose exec -T php-fpm composer install --no-interaction --working-dir=/var/www/symfony --no-dev
docker-compose exec -T php-fpm /bin/sh -c "cd /var/www/symfony && npm install && npm link webpack && npm run build"

# python module initiation
docker-compose exec -T crawler /bin/sh -c "cd /src && python docker_prepare_structure.py && python force_update_datasets.py all"
