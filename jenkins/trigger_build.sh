#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -f "$DIR/JENKINS_SERVER_URL" ]; then
    echo "JENKINS_SERVER_URL not found, copying default."
    cp "$DIR/JENKINS_SERVER_URL.default" "$DIR/JENKINS_SERVER_URL" 
fi

if [ ! -f "$DIR/JENKINS_SERVER_PORT" ]; then
    echo "JENKINS_SERVER_PORT not found, copying default."
    cp "$DIR/JENKINS_SERVER_PORT.default" "$DIR/JENKINS_SERVER_PORT" 
fi

SERVER_URL=$(cat "$DIR/JENKINS_SERVER_URL")
SERVER_PORT=$(cat "$DIR/JENKINS_SERVER_PORT")
REPO=$(git remote -v | grep "(fetch)" | cut -f2 | cut -f1 -d' ')
REPOS=$(echo "$REPO" | wc -l)

echoerr() { echo "$@" 1>&2; }

if [ $REPOS -ne 1 ]; then
    echoerr "More than one fetch repository"
    echoerr "Not supported."
    exit 1
fi

SERVER="http://${SERVER_URL}:${SERVER_PORT}"
URL="${SERVER}/git/notifyCommit?url=${REPO}"
curl $URL
