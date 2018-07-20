#!/bin/bash

FILES_USING_STR=$(\
./tools/find_files.py ".py" |\
 ./tools/filter_files.py "*/venv/*" "*/migrations/*" |\
 xargs grep "str(" |\
 cut -d':' -f1 |\
 sort |\
 uniq)

FILES_USING_UNICODE=$(\
./tools/find_files.py ".py" |\
 ./tools/filter_files.py "*/venv/*" "*/migrations/*" |\
 xargs grep "__unicode__" |\
 cut -d':' -f1 |\
 sort |\
 uniq)

EXIT_STATUS=0

if [ ! -z "$FILES_USING_STR" ]; then
    echo ""
    echo "The following files use 'str()' cast:"
    while read -r file; do
        echo -e "\t$file"
        EXIT_STATUS=1
    done <<< "$FILES_USING_STR"
    echo "Consider using 'smart_text()' instead."
    echo "See: https://docs.djangoproject.com/en/1.11/ref/utils/#django.utils.encoding.smart_text"
fi

if [ ! -z "$FILES_USING_UNICODE" ]; then
    echo ""
    echo "The following files use '__unicode__' member function:"
    while read -r file; do
        echo -e "\t$file"
        EXIT_STATUS=1
    done <<< "$FILES_USING_UNICODE"
    echo "Consider using '@python_2_unicode_compatible' instead."
    echo "See: https://docs.djangoproject.com/en/1.11/ref/utils/#django.utils.encoding.python_2_unicode_compatible"
fi

exit $EXIT_STATUS
