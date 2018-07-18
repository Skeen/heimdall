#!/bin/bash

EXIT_STATUS=0
 
GREP_COMMAND="pcregrep -Mn"
POST_COMMAND="sed 's/^\([0-9]*\):/On line: \1\n/g' | tr '\0' '\n'"
if ! [ -x "$(command -v pcregrep)" ]; then
    echo "Warning: pcregrep is not installed." >&2
    echo "         Falling back to GNU grep." >&2
    echo "" >&2
    GREP_COMMAND="grep -Pzo"
    POST_COMMAND="cat | tr '\0' '\n'"
fi

MISSING=$(cat locale/da_DK/LC_MESSAGES/django.po |\
          $GREP_COMMAND 'msgid.*\nmsgstr ""\n\n' |\
          eval $POST_COMMAND)
if [ -n "$MISSING" ]; then
    echo "Translations are missing within django.po"
    echo "$MISSING"
    echo ""
    EXIT_STATUS=$(($EXIT_STATUS || 1))
fi

FUZZY=$(cat locale/da_DK/LC_MESSAGES/django.po |\
        $GREP_COMMAND 'fuzzy\n(.|\n)*?\n\n' |\
        eval $POST_COMMAND)
if [ -n "$FUZZY" ]; then
    echo "Translations are fuzzy within django.po:"
    echo "$FUZZY"
    EXIT_STATUS=$(($EXIT_STATUS || 1))
fi

exit $EXIT_STATUS
