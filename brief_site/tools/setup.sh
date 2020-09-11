#!/bin/bash
set -e # fail on any error

MYSQL_PORT="$1"
WEB_PORT="$2"
HOST="$3"

if [ -n "$MYSQL_PORT" -a -n "$WEB_PORT" -a -n "$HOST" ]; then
    PWD=`pwd`
    cd `dirname $0`/..

    SUDO=''
    if [ "$(uname)" != 'Darwin' ]; then
        SUDO='sudo'
    fi

    find logs -type d | $SUDO xargs chmod 777

    # Copy env
    cp .env.local.example .env

    # Create docker dev
    sed -e "s/YOUR_MYSQL_PORT/$MYSQL_PORT/; s/YOUR_WEB_PORT/$WEB_PORT/" docker-compose.dev.yml.example > docker-compose.dev.yml

    npm install

    # Create nginx conf
    # In case of localhost or 127.0.0.1 replace blank
    if [ "$HOST" = "localhost" -o "$HOST" = "127.0.0.1" ]; then
        HOST=''
    fi
    sed -e "s/YOUR_HOST/$HOST/" web_server/dev_nginx.conf.template > web_server/default.conf

    cd $PWD
else
    echo 'Please enter mysql port, web port and host'
fi
