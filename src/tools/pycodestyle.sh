#!/bin/bash

./tools/find_files.py ".py" | \
 ./tools/filter_files.py "*/venv/*" "*/migrations/*" | \
 ./tools/filter_files.py "*/heimdall/settings*" |\
 ./tools/filter_files.py "*/licence/*" |\
 ./tools/filter_files.py "*/database/*" |\
 xargs flake8 --ignore=D105,D401,D100,D101,D102,D103,F841,E501,F401,E221,W291,W293,E129,E121,E122,E123,E124,E125,E126,E131,W503,F821,F403 $@
