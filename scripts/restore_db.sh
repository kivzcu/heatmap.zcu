#!/bin/bash

#
# TODO: set MongoDB credentials
#
docker-compose exec -T database mongorestore --username root --password root --authenticationDatabase admin --db open-data-db /dev-dump/data