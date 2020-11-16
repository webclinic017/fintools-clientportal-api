# Overview
Latest work in 'trader'.

# Ansible deployment

Run the playbook
```
cd ansible
ansible-playbook install-ib.yml
```


## Prerequisite on nodes (likely not needed)
/* NOT TRUE
On Debian.
```
apt-get install -y python-minimal
```
On CentOS it's more involved.
```
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
```
NOT TRUE */

# Operation
Consists of:

- downloader.py: download symbols, conids, quotes (3679 of them)
-- conids are fast to download
-- quotes are for today's price
- downloader-day.py: for cheap tickers (defined in config, e.g. less than $3/share, download today's data)

## downloader.py
Run this once a day or less.  

It does:
- get NASDAQ tickers
- download cnids: convert tickers to conids
- download quotes

Conids are saved to:

- /opt/fintools-ib/data/conids

The conids are what IB uses instead of tickers, such as AAPL.

## downloader-day.py
?

# IB

# App
```
curl http://app-addr/lt/10 | jq '.'
```
