#!/bin/sh
if [ -z $1 ]; then echo Missing argument && exit 1; fi
if [ -z $2 ]; then echo Missing argument && exit 1; fi
if [ -z $3 ]; then echo Missing argument && exit 1; fi

TIMEOUT=$1
ADDR=$2
PORT=$3
shift 3
CMD=$@

SECONDS=1

while :; do
  echo Attempt connect to $ADDR $PORT
  SECONDS=$(( SECONDS + 1 ))
  if nc -z -w 2 $ADDR $PORT ; then
    echo SUCCESS: Connected to $ADDR $PORT
    break
  fi
  if [ $SECONDS -gt $TIMEOUT ]; then
    echo ERROR: $ADDR port $PORT timed out
    exit 1
  fi
  sleep 1
done

echo EXECUTE: $CMD
$CMD
