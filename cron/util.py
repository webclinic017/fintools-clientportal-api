import ib_web_api
import json
import os
import sys
# IB
from ib_web_api import SessionApi
from ib_web_api.rest import ApiException
# Local

def is_running(pidfile):
  if os.path.isfile(pidfile):
    return True
  else:
    return False

def create_pid(pidfile):
  open(pidfile, 'w').write(str(os.getpid()))

def remove_pid(pidfile):
  os.unlink(pidfile)

def check_ib_connectivity():
  try:
    # Instantiate API class
    config = ib_web_api.Configuration()
    config.verify_ssl = False
    client = ib_web_api.ApiClient(config)
    api = SessionApi(client)
    res = api.iserver_auth_status_post()
  except Exception as e:
    raise('No IB connectivity')
