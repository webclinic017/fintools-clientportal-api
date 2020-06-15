# Plan
goal: trade $1 daily

TODO, components:
- mongo
- day1: daily record data
- day2: trader

# Overview
- s5: trade open based on previous day close

## s5: trade prev close
deadline: end of April  
goal: trade $1 every day

day1, after close:
  - goal/summary: find s to trade, get buy price
  - API PRIV: get s under $2
  - API PRIV: for each, find 4% increases
  - choose s where count(4%) > 0
  - record close price
  - data:
    prev_signals: {
      YYYYMMDD: { open:, high:, low:, close:, volume:,
        perc: [
          {
            buy: { price:, open:,high:, low:, close:, volume: },
            sell: {...}
            perc:
          },
          {...},
          {...}
        ]
      },
      YYYYMMDD: {...}
    }
  - chose SINGLE stock (e.g. chose highest vol)
day2:
  - input: { symbol: price, symbol: price }
  - how many symbols allowed? just one per day, or all?
    just one to begin with, ensure in aboe
    - loop, for symbol, STATES:
      - put in limit order
      - wait for fill, check portfolio
      - filled: exit strategy:
        - sell limit order for +4%
        - if 30 min before end of market day, cancel order, sell market
        - wait for fill
