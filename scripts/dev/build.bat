docker-compose -f docker-compose.yml -f docker-compose-dev.yml up --build -d
docker-compose exec php-fpm composer config extra.symfony.allow-contrib true --no-interaction --working-dir=/var/www/symfony
docker-compose exec php-fpm composer install --no-interaction --working-dir=/var/www/symfony
docker-compose exec php-fpm composer update --no-interaction --working-dir=/var/www/symfony
docker-compose exec php-fpm /bin/sh -c "cd /var/www/symfony && npm install && npm link webpack && npm run build"
docker-compose exec crawler /bin/sh -c "cd /src && python docker_prepare_structure.py && python force_update_datasets.py all"
