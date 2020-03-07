#!/bin/bash
# Skip first and last line headers
tail -n +2 nasdaqlisted.txt \
  | head -n -1 \
  | cut -d'|' -f1
