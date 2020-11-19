# Overview
Latest work in 'trader'.

# Ansible deployment

Run the playbook
```
cd ansible
ansible-playbook install-ib.yml
```

# Operation
Consists of:

- **downloader.py**: download symbols, conids, quotes (3679 of them)
    - conids: fast to download
    - quotes: for today's price: quotes should be previous day price, generate them after market close
- **downloader-day.py**: for cheap tickers (defined in config, e.g. less than $3/share, download today's data)

## dashboard
http://fintools-ib:8080/
```
service fintools-ib-dashboard status
```

## downloader.py
Run this once a day or less.  

It does:
- get NASDAQ tickers
- download conids: convert tickers to conids
- download quotes

Conids are saved to:

- /opt/fintools-ib/data/conids

The conids are what IB uses instead of tickers, such as AAPL.

## downloader-day.py
?

# IB
Check service running, or run it
TODO: Make this a service.
```
cd /opt/ib-gw
./bin/run.sh root/conf.yaml >> /var/log/ib-gw.log &
```

# App
```
curl http://app-addr/lt/10 | jq '.'
```
