#!/bin/bash

# Config:
# - DATA_DIR
# - QUOTE_DIR
. config.sh

# Helpers
get:conid() {
  # Get it from already downloaded
  :
}

#echo Get NASDAQ tickers file
#./get_symbols_file.sh &>/dev/null
#echo Filter file to get symbols only
#./get_symbols.sh &>/dev/null
#echo Filter to get only symbols which are in IB and get conids
#./get_symbols_ib.sh
#
#
#echo Download conids
## Filter to get only symbols which are in IB and get conids
#IN_FILE=data_sh/nasdaq_symbols
#OUT_FILE=data_sh/nasdaq_symbols_ib_conids
#if [[ -f $OUT_FILE ]]; then
#  rm $OUT_FILE
#fi
#touch $OUT_FILE
#
#while read I; do
#  CONID=$(./down_conid.py $I &>/dev/null)
#  if [[ $? == 0 ]]; then
#    echo $I $CONID
#    echo $I $CONID >> $OUT_FILE
#  fi
#done < $IN_FILE
#
#echo Download quotes
#if [[ -d $QUOTE_DIR ]]; then
#  rm -rf $QUOTE_DIR
#fi
#mkdir $QUOTE_DIR
#
#IN_FILE=$DATA_DIR/nasdaq_symbols_ib_conids
#while read SYMB CONID; do
#  ./down_quote.sh $CONID > $QUOTE_DIR/$SYMB.json
#  if [[ $? != 0 ]]; then
#    echo Could not get ticker $SYMB ($CONID)
#  fi
#done < $IN_FILE

LT=1
echo Find less than $LT close
./get_close_lt.sh c $LT
