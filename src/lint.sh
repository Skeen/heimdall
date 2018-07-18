#!/usr/bin/env bash

./tools/find_files.py ".py" --paths "." |\
 ./tools/filter_files.py "*/docs/*" "*/venv/*" "*/migrations/*" "*/tests/*" |\
 ./tools/filter_files.py "*/heimdall/settings*" |\
 ./tools/filter_files.py "*/licence/*" |\
 ./tools/filter_files.py "*/database/*" |\
 ./tools/filter_files.py "*/frontend/node_modules/*" |\
xargs pylint -r n --load-plugins pylint_django --load-plugins=missing_gettext --rcfile=.pylint $@
