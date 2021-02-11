#!/bin/bash
# Usage
# if you want create new license run: renew_certificate new
# if you want re-create the existing license run: renew_certificate

#
# TODO: set website domain
#
if [ "$1" = "new" ]; then
    docker-compose exec nginx /bin/sh -c "
    cd /root/.acme.sh; \
    bash acme.sh  --issue --nginx /etc/nginx/sites-available/default.conf -d heatmap.zcu.cz -d www.heatmap.zcu.cz --debug 2; \
    bash acme.sh --installcert -d heatmap.zcu.cz -d www.heatmap.zcu.cz\
    --key-file /root/.acme.sh/heatmap.zcu.cz/heatmap.zcu.cz.key \
    --fullchain-file /root/.acme.sh/heatmap.zcu.cz/fullchain.cer \
    --reloadcmd 'bash /etc/init.d/nginx reload';
    ";
else
    docker-compose exec nginx /bin/sh -c "cd /root/.acme.sh && bash acme.sh --issue --force -d heatmap.zcu.cz -d www.heatmap.zcu.cz -w /var/www/symfony/public && nginx -s reload"
fi
