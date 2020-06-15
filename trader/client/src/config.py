import configparser
class Config:
  main = []
  def __init__(self):
    config = configparser.ConfigParser()
    config.read('config.ini')
    self.main = config['main']

  def get(self, name):
    return self.main[name]
