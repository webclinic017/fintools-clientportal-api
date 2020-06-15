# Run this after close
from config import Config
config = Config()
ib_url = config.get('ib_url')
print(ib_url)

# goal/summary: find s to trade, get buy price
# API PRIV: get s under $2
# API PRIV: for each, find 4% increases
# choose s where count(4%) > 0
# record close price

