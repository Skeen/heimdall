#!/bin/bash

# Empty DB
python manage.py flush

# Make migrations
python manage.py makemigrations

# Migrate
python manage.py migrate
