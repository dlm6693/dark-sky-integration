from .process import DataProcessor, DataIngestor
from .fetch import Fetch
import asyncio
import os
import pandas as pd

class MasterCrawler(object):
    
    def __init__(self, key, mapping_data):
        self.mapping_data = mapping_data
        self.key = key
    
    def crawl(self):
        fetch = Fetch(self.mapping_data)
        # calling main
        if __name__ == 'api_data.master_crawler':
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