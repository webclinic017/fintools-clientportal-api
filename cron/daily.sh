#!/bin/bash
# Run this daily on cron
# Requirement: /etc/fintools-ib/config.sh

# Helpers
function log() {
  DATE=$(date +'%Y-%m-%d %H:%M')
  echo $DATE: $@
}

log Start $0
cd "$(dirname "$0")"
cd ..

# Config:
# - D_DATA
# - D_QUOT
. /etc/fintools-ib/config.sh

# Supress warnings
./bin/supress_source_me.sh
export PYTHONWARNINGS="ignore:Unverified HTTPS request"

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
[[ -f $OUT_FILE.tmp ]] && rm $OUT_FILE.tmp
while read I; do
  CONID=$($D_BIN/down_ticker2conid.py $I)
  if [[ $? == 0 ]]; then
    echo $I $CONID >> $OUT_FILE.tmp
  fi
done < $IN_FILE
if [[ $(wc -l $OUT_FILE.tmp | cut -d' ' -f1) == 0 ]]; then
  log None of the symbols are available in IB. Check your IB connection
  exit 1
fi
wc -l $OUT_FILE.tmp
mv $OUT_FILE{.tmp,}

log Download quote from conids
IN_FILE=$D_DATA/nasdaq_symbols_ib
OUT_FILE=$D_DATA/nasdaq_symbols_ib_conids
[[ -f $OUT_FILE.tmp ]] && rm $OUT_FILE.tmp
while read I; do
  CONID=$($D_BIN/down_conid2quote.sh $I &>/dev/null)
  [[ $? == 0 ]] && echo $I $CONID >> $OUT_FILE.tmp
done < $IN_FILE
if [[ $(wc -l $OUT_FILE.tmp | cut -d' ' -f1) == 0 ]]; then
  log Could not get IB conids for any of the stocks
  exit 1
fi
wc -l $OUT_FILE.tmp
mv $OUT_FILE{.tmp,}

log Download quotes
[[ -d $D_QUOT.tmp ]] && rm -rf $D_QUOT.tmp
mkdir $D_QUOT.tmp
IN_FILE=$D_DATA/nasdaq_symbols_ib_conids
while read SYMB CONID; do
  $D_BIN/down_conid2quote.sh $CONID > $D_QUOT.tmp/$SYMB.json
  [[ $? != 0 ]] && log Could not get ticker $SYMB \($CONID\)
done < $IN_FILE
COUNT=$(ls $D_QUOT.tmp | wc -l)
if [[ $COUNT ==  0 ]]; then
  log Could not get any quotes
  exit 1
fi
echo $COUNT

[[ -d $D_QUOT ]] && rm -rf $D_QUOT
mv $D_QUOT{.tmp,}

log Finished $0
