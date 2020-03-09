#!/bin/bash

DATE=$(date +'%Y-%m-%d %H:%M')
echo $DATE: Starting $0
cd "$(dirname "$0")"

# Config:
# - D_DATA
# - D_QUOT
. config.sh
. ../supress_source_me.sh

echo Get NASDAQ tickers file
curl --silent -o $D_DATA/nasdaq_file \
  ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt
wc -l $D_DATA/nasdaq_file

echo Filter file to get symbols only
# Skip first and last line headers
tail -n +2 $D_DATA/nasdaq_file \
  | head -n -1 \
  | cut -d'|' -f1 \
  > $D_DATA/nasdaq_symbols
wc -l $D_DATA/nasdaq_symbols

echo Filter to get only symbols which are in IB and get conids \(SLOW\)
IN_FILE=$D_DATA/nasdaq_symbols
OUT_FILE=$D_DATA/nasdaq_symbols_ib
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
wc -l $OUT_FILE

echo Download conids
IN_FILE=$D_DATA/nasdaq_symbols
OUT_FILE=$D_DATA/nasdaq_symbols_ib_conids
[[ -f $OUT_FILE ]] && rm $OUT_FILE
touch $OUT_FILE
while read I; do
  CONID=$(./down_conid.py $I &>/dev/null)
  [[ $? == 0 ]] && echo $I $CONID >> $OUT_FILE
done < $IN_FILE
if [[ $(wc -l $OUT_FILE | cut -d' ' -f1) == 0 ]]; then
  echo Could not get IB conids for any of the stocks
  exit 1
fi
wc -l $OUT_FILE

echo Download quotes
[[ -d $D_QUOT ]] && rm -rf $D_QUOT
mkdir $D_QUOT
IN_FILE=$D_DATA/nasdaq_symbols_ib_conids
while read SYMB CONID; do
  ./down_conid2quote.sh $CONID > $D_QUOT/$SYMB.json
  [[ $? != 0 ]] && echo Could not get ticker $SYMB \($CONID\)
done < $IN_FILE
ls $D_QUOT | wc -l

DATE=$(date +'%Y-%m-%d %H:%M')
echo $DATE: Finished $0
