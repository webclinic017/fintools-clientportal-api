#!/bin/bash
# Run this daily on cron

# Helpers
function log() {
  DATE=$(date +'%Y-%m-%d %H:%M')
  echo $DATE: $@
}

log Starting $0
cd "$(dirname "$0")"
cd ..

# Config:
# - D_DATA
# - D_QUOT
. bin/config.sh

# Supress warnings
./bin/supress_source_me.sh
export PYTHONWARNINGS="ignore:Unverified HTTPS request"

if [[ -d $D_DATA ]]; then
  rm -r $D_DATA
fi
mkdir $D_DATA

log Get NASDAQ tickers file
curl --silent -o $D_DATA/nasdaq_file \
  ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt
wc -l $D_DATA/nasdaq_file

log Filter file to get symbols only
# Skip first and last line headers
tail -n +2 $D_DATA/nasdaq_file \
  | head -n -1 \
  | cut -d'|' -f1 \
  > $D_DATA/nasdaq_symbols
wc -l $D_DATA/nasdaq_symbols

log Filter to get only symbols which are in IB and get conids \(SLOW\)
IN_FILE=$D_DATA/nasdaq_symbols
OUT_FILE=$D_DATA/nasdaq_symbols_ib
[[ -f $OUT_FILE ]] && rm $OUT_FILE
touch $OUT_FILE
while read I; do
  CONID=$($D_BIN/down_ticker2conid.py $I)
  if [[ $? == 0 ]]; then
    echo $I $CONID >> $OUT_FILE
  fi
done < $IN_FILE
if [[ $(wc -l $OUT_FILE | cut -d' ' -f1) == 0 ]]; then
  log None of the symbols are available in IB. Check your IB connection
  exit 1
fi
wc -l $OUT_FILE

log Download quote from conids
IN_FILE=$D_DATA/nasdaq_symbols_ib
OUT_FILE=$D_DATA/nasdaq_symbols_ib_conids
[[ -f $OUT_FILE ]] && rm $OUT_FILE
touch $OUT_FILE
while read I; do
  CONID=$($D_BIN/down_conid2quote.sh $I &>/dev/null)
  [[ $? == 0 ]] && echo $I $CONID >> $OUT_FILE
done < $IN_FILE
if [[ $(wc -l $OUT_FILE | cut -d' ' -f1) == 0 ]]; then
  log Could not get IB conids for any of the stocks
  exit 1
fi
wc -l $OUT_FILE

log Download quotes
[[ -d $D_QUOT ]] && rm -rf $D_QUOT
mkdir $D_QUOT
IN_FILE=$D_DATA/nasdaq_symbols_ib_conids
while read SYMB CONID; do
  $D_BIN/down_conid2quote.sh $CONID > $D_QUOT/$SYMB.json
  [[ $? != 0 ]] && log Could not get ticker $SYMB \($CONID\)
done < $IN_FILE
ls $D_QUOT | wc -l

log Finished $0
