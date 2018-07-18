#!/bin/bash

RUN_NEEDED=$(./manage.py makemigrations --dry-run | grep "No changes detected")

if [ -z "$RUN_NEEDED" ]; then
    echo "Needs to run 'python manage.py makemigrations'".
    exit 1
fi
