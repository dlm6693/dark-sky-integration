from .master_crawler import MasterCrawler
from redis import Redis
from rq import Queue
import pandas as pd
from dark_sky_app import settings
import os

key_path = os.path.join(settings.BASE_DIR, 'api_data/secret_key.txt')
with open(key_path, "r") as f:
    key = f.read()
loc_data = pd.read_csv("api_data/uscities.csv")
lat_long = loc_data[["lat", "lng"]][:100]
mc = MasterCrawler(mapping_data = lat_long, key=key)
redis_conn = Redis()
q = Queue(connection=redis_conn)
result = q.enqueue(func=mc.crawl, args=None, timeout=30)

https://github.com/rq/django-rq