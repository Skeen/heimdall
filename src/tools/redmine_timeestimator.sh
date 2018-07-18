#!/bin/bash

# Download the site:
# https://redmine.magenta-aps.dk/projects/ubs-sprint-3/agile/board
# as 'a.html' and run './redmine_timeestimator.sh'

cat a.html | grep 'class="hours"' | sed "s#.*>(\(.*\)h)<.*#\1#g" | sed 's#\(.*\)/\(.*\)#\2\t\1#g' | awk '{ SUM+=$1; WORK+=$2 } END {print WORK, "of", SUM, "=", SUM-WORK }'
