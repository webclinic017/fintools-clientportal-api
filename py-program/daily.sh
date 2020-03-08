#!/bin/bash

# Config:
# - DATA_DIR
# - QUOTE_DIR
. config.sh

echo Get NASDAQ tickers file
curl -o $DATA_DIR/nasdaq_file \
  ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt

echo Filter file to get symbols only
# Skip first and last line headers
tail -n +2 $DATA_DIR/nasdaq_file \
  | head -n -1 \
  | cut -d'|' -f1 \
  > data_sh/nasdaq_symbols

echo Filter to get only symbols which are in IB and get conids
IN_FILE=$DATA_DIR/nasdaq_symbols
OUT_FILE=$DATA_DIR/nasdaq_symbols_ib
[[ -f $OUT_FILE ]] && rm $OUT_FILE
touch $OUT_FILE
while read I; do
  CONID=$(./down_ticker2conid.py $I)
  if [[ $? == 0 ]]; then
    echo $I $CONID >> $OUT_FILE
  fi
done < $IN_FILE
if [[ $(wc -l $OUT_FILE | cut -d' ' -f1) == 0 ]]; then
  echo None of the symbols are available in IB. Check your IB connection
  exit 1
fi


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
  [[ $? != 0 ]] && echo Could not get ticker $SYMB \($CONID\)
done < $IN_FILE
