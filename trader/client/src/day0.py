from config import Config
config = Config()
ib_url = config.get('ib_url')
print(ib_url)
