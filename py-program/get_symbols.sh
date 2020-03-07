#!/bin/bash
# Skip first and last line headers
tail -n +2 data_sh/nasdaq_file \
  | head -n -1 \
  | cut -d'|' -f1 \
  > data_sh/nasdaq_symbols
