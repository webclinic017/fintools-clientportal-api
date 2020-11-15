import ib_web_api
import json
import os
import sys
# IB
from ib_web_api import SessionApi
from ib_web_api.rest import ApiException
# Local
import config

def is_running(pidfile):
  if os.path.isfile(pidfile):
    return True
  else:
    return False

def create_pid(pidfile):
  open(pidfile, 'w').write(str(os.getpid()))

def remove_pid(pidfile):
  os.unlink(pidfile)

def check_conidsfile(file_conids):
  with open(config.file_conids, 'w') as f:
    try:
      f = json.load(f)
    except Exception as e:
      # File in bad format, create empty
      conids = {}
      f.write(json.dumps(conids))

def check_ib_connectivity():
  # Instantiate API class
  config = ib_web_api.Configuration()
  config.verify_ssl = False
  client = ib_web_api.ApiClient(config)
  api = SessionApi(client)
  res = api.iserver_auth_status_post()
  print('RES', res)
