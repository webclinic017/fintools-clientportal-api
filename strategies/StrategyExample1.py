# Example strategy, a good example

import sys, os
from strategies.BaseStrategy import BaseStrategy

class StrategyExample1(BaseStrategy):
  def run(self):
    # Override the 'run' method of the base class
    print('I am example strategy')
