#!/bin/bash

find . -path "*/tests/*" -name "*.py" |\
 xargs pylint -r n --load-plugins pylint_django --rcfile=.pylint $@
