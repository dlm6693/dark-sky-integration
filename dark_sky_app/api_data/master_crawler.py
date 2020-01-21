from .process import DataProcessor, DataIngestor
from .fetch import Fetch
import asyncio

#open secret key
with open("secret_key.txt", "r") as f:
    key = f.read()
    
# open location data file
loc_data = pd.read_csv("uscities.csv")

# pull out only lat/long cols and limit to 1000 rows for API call
lat_long = loc_data[["lat", "lng"]][:1000]

fetch = Fetch(mapping_data=lat_long)

class MasterCrawler(object):
    
    def __init__(self, mapping_data):
        self.mapping_data = mapping_data
    
    def crawl(self):
        fetch = Fetch(self.mapping_data)
        # calling main
        if __name__ == "__main__":
            self.response_data = asyncio.run(fetch.main(url_template=fetch.template, secret_key=key, loc_data=self.mapping_data, exclude_args = fetch.exclude))
        
        processor = DataProcessor(self.response_data)
        processed_data = processor.process()
        
        ingestor = DataIngestor()
        
        for key, value in processed_data.items():
            ingestor.ingest(df=value, table_name=key)