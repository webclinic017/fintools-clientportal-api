#!/bin/bash
# Get stocks whose open/high/low/close (OHLC) price is less than PRICE
# ./get_close_lt o/h/l/c PRICE

# Config:
# - DATA_DIR
# - QUOTE_DIR
. config.sh

usage() {
  echo ./get_close_lt o/h/l/c PRICE
}

[[ -z $1 ]] && usage && exit 1
[[ -z $2 ]] && usage && exit 1
LT=1
for I in $QUOTE_DIR/*; do
  CLOSE=$(jq '.c' $I)
  if (( $(echo "$CLOSE <= $LT" | bc -l) )); then
    echo $(basename $I .json): $CLOSE
  else
    :
  fi
done
