#!/bin/bash

# Always build the frontend before starting server
./build_frontend.sh

# Run server with output to 0.0.0.0:8000
cd ../../
python manage.py runserver 0.0.0.0:8000
