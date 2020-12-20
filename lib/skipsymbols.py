import json

# Local
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from lib.config import Config

# Config

class Skipsymbols:
  # Properties
  cfg = {}

  # Constructor
  def __init__(self):
    # Config
    cfg = Config()
    self.file_skipsymbols = cfg['paths']['file_skipsymbols']

    try:
      # Read file
      with open(self.file_skipsymbols, 'r') as f:
        symbols = json.load(f)
        if len(symbols) < 1:
          raise Exception('Too few skip symbols found')
    except Exception as e:
      raise Exception(e)


  # PUBLIC METHODS
  def get(self):
    # Get skip symbols list
    try:
      with open(self.file_skipsymbols, 'r') as f:
        return json.load(f)
    except Exception as e:
      raise Exception('Could not get skip symbols')

  def add(self, symbol):
    # Add to exclude list
    try:
      with open(self.file_skipsymbols, 'r+') as f:
        symbols = json.load(f)
        symbols.append(symbol)
        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(sorted(symbols), indent=2))
    except Exception as e:
      raise Exception('Could not get skip symbols:'+str(e))
    # TODO
    # open file
