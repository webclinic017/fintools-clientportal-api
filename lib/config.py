# imports: OS
import os.path
from configparser import ConfigParser
# imports: local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.constants import FILE_CFG

path_defaults = {
  'conids': '/conids',
  'contracts': '/data/contracts',
  'day': '/data/day',
  'quotes': '/data/quotes',
}

class Config(ConfigParser):
  # Constructor
  def __init__(self):
    ConfigParser.__init__(self)
    try:
      # Read config
      try:
        if os.path.isfile('/config.cfg'):
          # Dev config file is in root
          # use it if it exists
          fileCfg = '/config.cfg'
        else:
          # Prod config file is as specified in 'constants.py'
          fileCfg = FILE_CFG
        # Check file exists
        with open(fileCfg) as f:
          pass
      except IOError:
        raise Exception('Cannot read config file: %s' % fileCfg)
      dataset = self.read(fileCfg)
      if len(dataset) == 0:
        raise Exception('Could not read config file %s' % fileCfg)
      # Default paths
      base = self['paths']['base']
      for path_name, path in path_defaults.items():
        self['paths'].update({ path_name: base + path })
    except Exception as e:
      raise Exception(e)
