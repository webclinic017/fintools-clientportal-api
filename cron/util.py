import os
import sys

def is_running(pidfile):
  if os.path.isfile(pidfile):
    return True
  else:
    return False

def create_pid(pidfile):
  open(pidfile, 'w').write(str(os.getpid()))

def remove_pid(pidfile):
  os.unlink(pidfile)
