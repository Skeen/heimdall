#!/usr/bin/env bash

./tools/find_files.py ".html" |\
 ./tools/filter_files.py "*/docs/*" "*/venv/*" "*/migrations/*" "*/htmlcov/*" |\
 ./tools/filter_files.py "*/frontend/node_modules/*" "*/static/*"|\
 xargs python -m django_template_i18n_lint |\
 sed 's/\(.*\):\(.*\)$/\1: W9993 Missing translation; "\2"/g'
