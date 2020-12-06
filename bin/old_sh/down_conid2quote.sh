#!/bin/bash
# $1: CONID
# e.g. conid for AAPL: 209011562
# Exqmple: ./get_quote 209011562

[[ -z $1 ]] && echo No conid && exit 1
CONID=$1

URL="https://localhost:5000\
/v1/portal/iserver/marketdata/history\
?conid=$CONID\
&period=3d&bar=1d"
DATA=$(curl -sk --connect-timeout 2 -X GET $URL \
  -H 'Content-Type: application/x-www-form-urlencoded')
POINT=$(jq -r '.points' <<< $DATA)
LAST_DATA=$(jq ".data[$POINT]" <<< $DATA)
echo $LAST_DATA
