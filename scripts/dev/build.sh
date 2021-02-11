#!/bin/bash
#Build development environment
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up --build -d
echo "================= BUILDING DONE ==================="
cat << "EOF"
 ______  ______  __    __  ______ ______  ______  ______  ______       __  __   __  ______  ______ ______  __      __
/\  ___\/\  __ \/\ "-./  \/\  == /\  __ \/\  ___\/\  ___\/\  == \     /\ \/\ "-.\ \/\  ___\/\__  _/\  __ \/\ \    /\ \
\ \ \___\ \ \/\ \ \ \-./\ \ \  _-\ \ \/\ \ \___  \ \  __\\ \  __<     \ \ \ \ \-.  \ \___  \/_/\ \\ \  __ \ \ \___\ \ \____
 \ \_____\ \_____\ \_\ \ \_\ \_\  \ \_____\/\_____\ \_____\ \_\ \_\    \ \_\ \_\\"\_\/\_____\ \ \_\\ \_\ \_\ \_____\ \_____\
  \/_____/\/_____/\/_/  \/_/\/_/   \/_____/\/_____/\/_____/\/_/ /_/     \/_/\/_/ \/_/\/_____/  \/_/ \/_/\/_/\/_____/\/_____/
EOF
docker-compose exec php-fpm composer config extra.symfony.allow-contrib true --no-interaction --working-dir=/var/www/symfony
docker-compose exec php-fpm composer update --no-interaction --working-dir=/var/www/symfony
docker-compose exec php-fpm composer install --no-interaction --working-dir=/var/www/symfony
echo "================= COMPOSER INSTALL DONE ==================="
cat << "EOF"
 ________    ________   _____ ______           ___   ________    ________   _________   ________   ___        ___
|\   ___  \ |\   __  \ |\   _ \  _   \        |\  \ |\   ___  \ |\   ____\ |\___   ___\|\   __  \ |\  \      |\  \
\ \  \\ \  \\ \  \|\  \\ \  \\\__\ \  \       \ \  \\ \  \\ \  \\ \  \___|_\|___ \  \_|\ \  \|\  \\ \  \     \ \  \
 \ \  \\ \  \\ \   ____\\ \  \\|__| \  \       \ \  \\ \  \\ \  \\ \_____  \    \ \  \  \ \   __  \\ \  \     \ \  \
  \ \  \\ \  \\ \  \___| \ \  \    \ \  \       \ \  \\ \  \\ \  \\|____|\  \    \ \  \  \ \  \ \  \\ \  \____ \ \  \____
   \ \__\\ \__\\ \__\     \ \__\    \ \__\       \ \__\\ \__\\ \__\ ____\_\  \    \ \__\  \ \__\ \__\\ \_______\\ \_______\
    \|__| \|__| \|__|      \|__|     \|__|        \|__| \|__| \|__||\_________\    \|__|   \|__|\|__| \|_______| \|_______|
                                                                   \|_________|
EOF
docker-compose exec -T php-fpm /bin/sh -c "cd /var/www/symfony && npm install && npm link webpack && npm run build"
echo "================= NPM INSTALL DONE ==================="
docker-compose exec -T crawler /bin/sh -c "cd /src && python docker_prepare_structure.py && python force_update_datasets.py all"
echo "================= LOADING DATASETS DONE ==================="
