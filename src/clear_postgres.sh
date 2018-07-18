#!/usr/bin/env bash

if [ $# -lt 3 ]
  then
    echo "Usage: clear_postgres.sh [port] [username] [database]"
fi

dropdb --host localhost --port $1 --username $2 $3
createdb --host localhost --port $1 --username $2 $3
