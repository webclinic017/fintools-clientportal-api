#!/bin/bash
# Skip first and last line headers
tail -n +2 data_sh/list \
  | head -n -1 \
  | cut -d'|' -f1
