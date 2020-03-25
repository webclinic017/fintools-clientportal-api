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
- 13:20 Sign in
- 13:25 Run downloader.py
- 13:30 Market open
- 13:31 Run download-day.py
- 13:40 Run download-day.py
- 14:00 Captured data. By now should have:
  - two symbols max <- at least once featured
  - entry price <- ?
  - exit price (+4%)
- 14:01 Buy order
- 14:02 Limit sell order (+4%)
