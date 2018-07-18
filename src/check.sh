#!/bin/bash

./compile_messages.sh >/dev/null
./find_missing_i18n.sh
./find_missing_translations.sh
./i18nlint_templates.sh
./lint.sh
./lint_tests.sh
./pycodestyle.sh
./tools/unicode_check.sh
./tools/reverse_model_checker.sh webapp/models/
./tools/reverse_model_checker.sh adminapp/models/
./tools/makemigrations_needed.sh
./licence/check_mapping.py
