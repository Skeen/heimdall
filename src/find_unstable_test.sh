#!/bin/bash

while true; do
    ./runtests.sh
    STATUS=$?
    if [ "$STATUS" -ne 0 ]; then
        echo "Test failed..."
        break
    fi
    coverage report | grep "[0-9][0-9]%"
    STATUS=$?
    if [ "$STATUS" -ne 0 ]; then
        echo "Coverage failed..."
        break
    fi
done
