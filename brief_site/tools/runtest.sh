#!/bin/sh
set -e

PWD=`pwd`
cd `dirname $0`/..

TEST_TARGET=
OPTS="-f docker-compose.yml -f docker-compose.test.yml"
COMMAND="run --rm --user=www-data"

if docker-compose $OPTS ps -q web > /dev/null 2>&1; then
    docker-compose $OPTS up -d web
    sleep 5
fi

# Use root account to assign permission create/drop database when running unit test
docker-compose exec mysql mysql -u root -ppassonate -e "GRANT ALL PRIVILEGES ON test_passonate.* TO 'passonate';"
docker-compose $OPTS $COMMAND django ./manage.py test $TEST_TARGET || echo done

cd $PWD
