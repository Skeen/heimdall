#!/bin/bash

TEMPLATES_USING_TRANS=$(\
./tools/find_files.py ".html" |\
 ./tools/filter_files.py "*/venv/*" "*/migrations/*" |\
 xargs grep "{% trans" |\
 cut -d':' -f1 |\
 sort |\
 uniq)

EXIT_STATUS=0
while read -r template; do
    cat "$template" | grep -q "{% load i18n %}"
    STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo "$template" misses translate header
        EXIT_STATUS=1
    fi

done <<< "$TEMPLATES_USING_TRANS"

exit $EXIT_STATUS
