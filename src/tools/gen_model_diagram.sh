#!/bin/bash
DIR="$(dirname "${BASH_SOURCE[0]}")"
python $DIR/../manage.py graph_models -a -g -o $DIR/../docs/_static/datamodel_generated.png
