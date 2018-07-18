#!/bin/bash

OUTPUT_DIR=_build

cd docs/

if [ -d "$OUTPUT_DIR" ]; then
    echo "Warning: Documentation found within $OUTPUT_DIR"
    echo "Warning: Cleaning..."
    echo ""
    rm -rf $OUTPUT_DIR
fi
cd ..

MAKE_OUTPUT=$(python manage.py build_docs 2>&1)
echo "$MAKE_OUTPUT"

ERROR_GREP=$(echo "$MAKE_OUTPUT" | grep "ERROR")
if [ -n "$ERROR_GREP" ]; then
    exit 1
fi
