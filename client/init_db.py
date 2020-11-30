# Create DB, tables etc
import inspect
import mysql.connector

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.config import Config
#from strategies import *
import strategies
#from lib.helpers import die

# CONFIG
syncFieldsFile = '../lib/ci_get_fields.yaml'

# LOAD ALL STRATEGIES
# TODO: This is barely working, duplicate name == BaseStrategy
# TODO: Fix this
print('Import strategies')
import os, sys
strategies = []
path = os.path.join(
  os.path.dirname(os.path.abspath(__file__)),
  '../strategies')
for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']:
  # Note: We actually have just a single class per module/file
  if py == 'BaseStrategy':
    continue
  print('Load:', py)
  pypath = '.'.join(['strategies', py])
  mod = __import__(pypath, fromlist=[py])
  classes = [getattr(mod, x)
    for x in dir(mod)
    if isinstance(getattr(mod, x), type)]
  for cls in classes:
    name = cls.__name__
    if name == 'BaseStrategy':
      continue
    strategies.append(name)
    setattr(sys.modules[__name__], name, cls)
print('Strategies loaded:', strategies)
# END LOAD ALL STRATEGIES

# Load classes
for strategy_name in strategies:
  strategy = eval(strategy_name)()
  print('Run:', strategy_name)
  strategy.run()
# TODO: Don't run run here


# MAIN
cfg = Config()

try:
  # Connect to DB server
  print('Initialise database')
  db_connection = mysql.connector.connect(
    host = cfg['db']['host'],
    user = cfg['db']['user'],
    passwd = cfg['db']['password']
  )
  db_cursor = db_connection.cursor()

  # Create DB
  db_cursor.execute('CREATE DATABASE fintools')
  # List databases
  db_cursor.execute("SHOW DATABASES")
  for db in db_cursor:
    print(db)

  # Create tables

  # TODO: Add strategies to DB
except Exception as e:
  print(e)
  exit(1)
