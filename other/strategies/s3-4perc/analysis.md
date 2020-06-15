# Analysis

Ideas:
1. gather data until 14:00, then trade  
2. use prev close, trade on open

# Overview
We have 5 days of data:
- 20200320 Fri
- 20200324 Tue
- 20200325 Wed
- 20200326 Thu
- 20200330 Mon

# 1
How many opportunities:  
## HTBX  
CT: total no. of opportunities in a day  
C1: # oports before 14:00  
C2: # oports after 14:00  

DATE     CT C1 C2
20200320 10 5  5
20200324 1  1  0
20200325 17 4  13
20200326 12 4  8
20200330 5  5  0

## MHLD

- HTBX: 10
- MHLD: 45

This didn't work, eventually these were squeezed to within first 30 mins of open for 4%.
3% is still work looking at. Focusing on #2 instead.

# 2. Use prev close, trade on open
In #1 found symbols:
- GRNVR
- HTBX
- MGI
- MHLD

over days:
20200320 Fr
20200324 Tu
20200325 We
20200326 Th
20200330 Mo
20200331 Tu
20200401 We
20200402 Th
20200403 Fr
20200406 Mo
20200407 Tu

so from 20200320-20200407  
The call /iserver/marketdata/history doesn't let specifying dates, so ignore the dates done so far in #1, and just do last month, but use the symbols from #1.

Plan:
- in: SYMBOLS, e.g. AA BB CC
- for each conid:
  - /iserver/marketdata/history with:
    - exchange: NASDAQ
    - period: 1m
    - bar: 5m
- for each day
