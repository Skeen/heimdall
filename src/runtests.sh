#!/bin/bash
# TODO: Unify with E2ETests

rm -rf .coverage
rm -rf .coverage.*
./tools/makemigrations_needed.sh
STATUS=$?
if [ $STATUS -ne 0 ]; then
    exit $STATUS
fi
python tools/runtests.py $@
coverage combine
