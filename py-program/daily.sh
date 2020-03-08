#!/bin/bash

# Config:
# - DATA_DIR
# - QUOTE_DIR
. config.sh

echo Get NASDAQ tickers file
wget -O data_sh/nasdaq_file \
  ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt \
  &>/dev/null

echo Filter file to get symbols only
./get_symbols.sh &>/dev/null
# Skip first and last line headers
tail -n +2 data_sh/nasdaq_file \
  | head -n -1 \
  | cut -d'|' -f1 \
  > data_sh/nasdaq_symbols

echo Filter to get only symbols which are in IB and get conids
IN_FILE=data_sh/nasdaq_symbols
OUT_FILE=data_sh/nasdaq_symbols_ib
[[ -f $OUT_FILE ]] && rm $OUT_FILE
touch $OUT_FILE
while read I; do
  CONID=$(./get_conid_nasdaq.py $I &>/dev/null)
  if [[ $? == 0 ]]; then
    echo $I $CONID >> $OUT_FILE
  fi
done < $IN_FILE

echo Download conids
# Filter to get only symbols which are in IB and get conids
IN_FILE=data_sh/nasdaq_symbols
OUT_FILE=data_sh/nasdaq_symbols_ib_conids
[[ -f $OUT_FILE ]] && rm $OUT_FILE
touch $OUT_FILE
while read I; do
  CONID=$(./down_conid.py $I &>/dev/null)
  [[ $? == 0 ]] && echo $I $CONID >> $OUT_FILE
done < $IN_FILE

echo Download quotes
[[ -d $QUOTE_DIR ]] && rm -rf $QUOTE_DIR
mkdir $QUOTE_DIR
IN_FILE=$DATA_DIR/nasdaq_symbols_ib_conids
while read SYMB CONID; do
  ./down_conid2quote.sh $CONID > $QUOTE_DIR/$SYMB.json
  [[ $? != 0 ]] && echo Could not get ticker $SYMB ($CONID)
done < $IN_FILE
