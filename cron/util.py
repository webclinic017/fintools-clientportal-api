import json
import os
import sys
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
