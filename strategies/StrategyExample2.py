# Example strategy, a bad example
# It did not override the 'run' from BaseStrategy
# Don't do this

import sys, os
from strategies.BaseStrategy import BaseStrategy

class StrategyExample2(BaseStrategy):
  pass
  #def __init__(self):
  #    self.name= "Circle"
  #    self.data= ["Radius: ", radius]
