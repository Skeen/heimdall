#!/usr/bin/env bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$PROJECT_DIR/manage.py makemessages --all --ignore "htmlcov/*.html" --no-location
MAKE_MESSAGES_CHECK=$?
$PROJECT_DIR/manage.py compilemessages
COMPILE_MESSAGES_CHECK=$?

# Remove slack from .po file
DK_TRANS=$PROJECT_DIR/locale/da_DK/LC_MESSAGES/django.po
sed -i '/"Report-Msgid-Bugs-To:.*"/d' $DK_TRANS
sed -i '/"POT-Creation-Date:.*"/d' $DK_TRANS

exit $MAKE_MESSAGES_CHECK || $COMPILE_MESSAGES_CHECK
