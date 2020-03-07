#!/bin/bash
echo Get NASDAQ tickers file
./get_symbols_file.sh &>/dev/null
echo Filter file to get symbols only
./get_symbols.sh &>/dev/null
echo Filter to get only symbols which are in IB and get conids
./get_symbols_ib.sh
