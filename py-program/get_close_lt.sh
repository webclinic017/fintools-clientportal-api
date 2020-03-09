#!/bin/bash
# Get stocks whose open/high/low/close (OHLC) price is less than PRICE
# ./get_close_lt o/h/l/c PRICE

# Config:
# - D_DATA
# - D_QUOT
. config.sh

usage() {
  echo ./get_close_lt o/h/l/c PRICE
}

[[ -z $1 ]] && usage && exit 1
[[ -z $2 ]] && usage && exit 1
TYPE=$1
PRICE=$2

for I in $D_QUOT/*; do
  STOCK_PRICE=$(jq ".$TYPE" $I)
  if (( $(echo "$STOCK_PRICE <= $PRICE" | bc -l) )); then
    echo $(basename $I .json): $STOCK
  else
    :
  fi
done
