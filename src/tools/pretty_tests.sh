#!/bin/bash

## Colors
##-------
BLACK=$(tput setaf 0)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
LIME_YELLOW=$(tput setaf 190)
POWDER_BLUE=$(tput setaf 153)
BLUE=$(tput setaf 4)
MAGENTA=$(tput setaf 5)
CYAN=$(tput setaf 6)
WHITE=$(tput setaf 7)
BRIGHT=$(tput bold)
NORMAL=$(tput sgr0)
BLINK=$(tput blink)
REVERSE=$(tput smso)
UNDERLINE=$(tput smul)

## Size
##-----
LINES=$(tput lines)
COLUMNS=$(tput cols)

## Task function
##--------------
function task
{
    INFO_STRING=$1
    TEXT_LENGTH=${#INFO_STRING}
    MAX_SPACING=$(($COLUMNS<80?$COLUMNS:80))
    SPACES=`expr $MAX_SPACING - $TEXT_LENGTH`
    printf "$INFO_STRING"
    STATUS=$2
    if [ $STATUS -eq 0 ]; then
        printf "%${SPACES}s" "${GREEN}[OK]${NORMAL}"
    else
        printf "%${SPACES}s" "${RED}[FAIL]${NORMAL}"
    fi
    printf "\n"
}

while read line; do

    TEST_NAME=$(echo "$line" | cut -f1 -d' ')
    STATUS=$(echo "$line" | cut -f2 -d' ')
    task $TEST_NAME $STATUS
done < "${1:-/dev/stdin}"
