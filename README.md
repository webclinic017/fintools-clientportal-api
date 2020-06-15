# Overview
Latest work in 'trader'.

# Ansible deployment

Run the playbook
```
cd ansible
ansible-playbook install.yml
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
downloader.py downloads data for all tickers.  
then we can find cheap tickers
