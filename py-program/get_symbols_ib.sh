#!/bin/bash
# Filter to get only symbols which are in IB and get conids
IN_FILE=data_sh/nasdaq_symbols
OUT_FILE=data_sh/nasdaq_symbols_ib
if [[ -f $OUT_FILE ]]; then
  rm $OUT_FILE
fi
touch $OUT_FILE

while read I; do
  CONID=$(./get_conid_nasdaq.py $I &>/dev/null)
  if [[ $? == 0 ]]; then
    echo $I $CONID >> $OUT_FILE
  fi
done < $IN_FILE
