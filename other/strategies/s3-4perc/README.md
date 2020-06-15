Given a list of tickers, return tickers which spiked X% at some time.

# TODO
- Add monitor script
- Add watcher script
- Add autotrade
- download-day.py should write json data out
- downloader.py should save data to date dir
- new download-day.py for one or two stocks only

# Playbook
- 13:20 Sign in
- 13:30 Market open
- 13:31 Run watcher script
- 14:00 Captured data. By now should have:
  - two symbols max <- at least once featured
  - entry price <- ?
  - exit price (+4%)
- 14:01 Buy order
- 14:02 Limit sell order (+4%)

TODO:
- how long wait?

# Pre playbook
- 09:00 Sign in, check health http://5.152.176.191/health
- 09:01 Run downloader.py
- ...
- 13:20 Sign in, check health http://5.152.176.191/health
- 13:20 https://degiro.co.uk/
- 13:30 Market open
- 13:45 Run download-day.py (15 min delay)
- 13:50 Run download-day.py (15 min delay)
- 13:51 Run download-day.py (with tickers)
- 14:00 Captured data. By now should have:
  - two symbols max <- at least once featured
  - entry price <- ?
  - exit price (+4%)
- 14:01 Buy order
- 14:02 Limit sell order (+4%)

# Playbook
- test cases
- run downloader
