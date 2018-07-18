#!/bin/bash
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DK_TRANS=$PROJECT_DIR/locale/da_DK/LC_MESSAGES/django.po

TMP_FILE=$(mktemp)

./tools/duplicate_cleaner.py $DK_TRANS > $TMP_FILE
cp $TMP_FILE $DK_TRANS
sed -i "s/^#~.*//g" $DK_TRANS
