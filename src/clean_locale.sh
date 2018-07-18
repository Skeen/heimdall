#!/bin/bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DK_TRANS=$PROJECT_DIR/locale/da_DK/LC_MESSAGES/django.po

sed "/<<<<<<< HEAD/d" -i $DK_TRANS
sed "/=======/d" -i $DK_TRANS
sed "/>>>>>>> .*/d" -i $DK_TRANS

./remove_locale_duplicates.sh
./compile_messages.sh
