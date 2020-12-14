# Overview
Latest work in 'trader'.

# Quick urls
These are for my own use.

- dashboard: http://192.168.0.100:8080: `cd /opt/fintools-ib/dashboard; node server.js &`
- API: http://192.168.0.100/, service fintools-ib, logs in /var/log/uwsgi. flask + uwsgi + nginx
- IB-gw service: `cd /opt/ib-gw; ./bin/run.sh root/conf.yaml >> /var/log/ib-gw.log &`

Useful urls
- http://192.168.0.100/health
- http://192.168.0.100/lt/3

## Docker
Start services.
```
dc build
dc up
./docker-stop.sh
```

The urls:  
- API: http://localhost:8000/
- Grafana: http://localhost:8001/
- dashboard: http://localhost:8002/
- db: localhost:8003

# Ansible deployment

Run the playbook
```
cd ansible
ansible-playbook install-ib.yml
```

# Operation
Consists of:

- **download-conids-quotes.py**: download symbols, conids, quotes (3679 of them)
    - conids: fast to download
    - quotes: for today's price: quotes should be previous day price, generate them after market close
- **download-day.py**: for cheap tickers (defined in config, e.g. less than $3/share, download today's data/prices)

## dashboard
http://fintools-ib:8080/
```
service fintools-ib-dashboard status
```



## download-conids-quotes.py
Run this once a day or less.  

It does:
- get NASDAQ tickers
- download conids: convert tickers to conids
- download quotes

Conids are saved to:

- /opt/fintools-ib/data/conids

The conids are what IB uses instead of tickers, such as AAPL.

## download-day.py
?

# IB
Check service running, or run it
TODO: Make this a service.
```
cd /opt/ib-gw
./bin/run.sh root/conf.yaml >> /var/log/ib-gw.log &
```

# fintools-ib: App (API)
```
curl http://app-addr:80/lt/10 | jq '.'
```
