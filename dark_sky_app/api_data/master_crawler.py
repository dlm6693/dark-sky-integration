from .process import DataProcessor, DataIngestor
from .fetch import Fetch
import asyncio
from dark_sky_app.dark_sky_app import settings
import os
import pandas as pd

#open secret key
key_path = os.path.join(settings.BASE_DIR, 'api_data/secret_key.txt')
with open(key_path, "r") as f:
    key = f.read()
    
# open location data file
loc_data = pd.read_csv("uscities.csv")

# pull out only lat/long cols and limit to 1000 rows for API call
lat_long = loc_data[["lat", "lng"]][:1000]

fetch = Fetch(mapping_data=lat_long)

class MasterCrawler(object):
    
    def __init__(self, key, mapping_data):
        self.mapping_data = mapping_data
        self.key = key
    
    def crawl(self):
        fetch = Fetch(self.mapping_data)
        # calling main
        
        response_data = asyncio.run(fetch.main(
                url_template=fetch.template, 
                secret_key=self.key, 
                loc_data=self.mapping_data, 
                exclude_args = fetch.exclude_args))
        
        processor = DataProcessor(response_data)
        processed_data = processor.process()
        
        ingestor = DataIngestor()
        
        for key, value in processed_data.items():
            ingestor.ingest(df=value, table_name=key)
        
        ingestor.dispose_and_close()