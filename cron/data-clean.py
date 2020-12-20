#!/usr/bin/env python3
# Download list of nasdaq symbols
# The symbols which don't exist, delete data from conids, quotes etc dirs
# Run once a week

# OS
import json
from traceback import print_exc

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.company import Company
from lib.config import Config
from lib.util import down_symbols
from lib.util import get_contracts
from lib.util import get_quotes
from lib.util import get_symbols
from lib.util import log


### MAIN ###
log('Start')

# Read config
cfg = Config()
dir_conids = cfg['paths']['conids']
dir_contracts = cfg['paths']['contracts']
dir_quotes = cfg['paths']['quotes']
debug = cfg.getboolean('main', 'debug')

log('Down NASDAQ symbols')
symb_nasdaq = down_symbols(cfg, apply_filters=False)
count_total = len(symb_nasdaq)
log('Got %i symbols in NASDAQ' % count_total)

log('Clean conids')
conids_disk = get_symbols()
log('Got %i conids' % len(conids_disk))
for conid in conids_disk:
  if conid not in symb_nasdaq:
    conid_path = dir_conids + '/' + conid
    print('Delete conid %s' % conid_path)
    os.remove(conid_path)

log('Clean contracts')
disk = get_contracts()
log('Got %i contracts' % len(disk))
for name in disk:
  if name not in symb_nasdaq:
    path = dir_contracts + '/' + name + '.json'
    print('Delete contract %s' % path)
    os.remove(path)

log('Clean quotes')
disk = get_quotes()
log('Got %i quotes' % len(disk))
for name in disk:
  if name not in symb_nasdaq:
    path = dir_quotes + '/' + name + '.json'
    print('Delete quote %s' % path)
    os.remove(path)
