#!/bin/bash

FOLDER=$1

check_file()
{
    FILE=$1
    RELATED=$2
    FROM=$3

    if [ "$RELATED" == "+" ]; then
        #echo "Found related_name='+' : Skipping"
        return
    fi

    if [ ! -f $FOLDER/$FILE.py ]; then
        return
    fi

    if grep -q "# $RELATED = incoming foreign key from $FROM\$" \
        $FOLDER/$FILE.py; then
        return
    else
        printf '%-30s%-30s%-30s\n' $(echo "$FILE.py") $RELATED $FROM
    fi
}

# NOTE: This assumes that the first class in the file, is the model.
REVERSE=$(perl -0777 -ne 'my @wa = (/class (.*?)\(.*\):/sg); my @wo = (/(models.ForeignKey|models.OneToOneField|models.ManyToManyField)\((.*?),.*?related_name=(".*?"),?.*?\)/sg); print join(" ", @wa, @wo); print "\n"' $FOLDER/*.py)
REVERSE=$(echo "$REVERSE" | tr ' ' '@')

OUTPUT_LINES=""

FROM=""
while read -r line; do
    if [[ $line == @* ]]; then
        FILE=$(echo "$line" | sed 's/@@//g' | cut -d'@' -f1)
        RELATED=$(echo "$line" | sed 's/@@//g' | cut -d'@' -f2 | sed 's/"//g' | sed "s/'//g")
        OUTPUT=$(check_file $FILE $RELATED $FROM)
        if [ -n "$OUTPUT" ]; then
            OUTPUT_LINES="${OUTPUT_LINES}${OUTPUT}"
        fi
    else
        FROM=$(echo "$line" | cut -d'@' -f1)
    fi   
done <<< "$REVERSE"

if [ -z "$OUTPUT_LINES" ]; then
    exit 0
else
    printf '%-30s%-30s%-30s\n' "Filename" "related_name" "Missing type"
    printf '=%.0s' {1..90}
    echo ""

    echo "$OUTPUT_LINES"

    echo ""
    echo "^^-- Files which are missing related_name comment (with Type) --^^"
    echo "Folder checked: $FOLDER"

    exit 1
fi
