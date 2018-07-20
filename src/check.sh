#!/bin/bash

./tools/compile_messages.sh >/dev/null
./tools/find_missing_translations.sh
./tools/lint.sh
# ./tools/lint_tests.sh
./tools/pycodestyle.sh
./tools/unicode_check.sh
./tools/reverse_model_checker.sh api/models/
./tools/makemigrations_needed.sh
./licence/check_mapping.py
