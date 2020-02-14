from api_data.master_crawler import MasterCrawler, DBConnector
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
if __name__ == '__main__':
    key = os.environ.get('DARK_SKY_SECRET_KEY')
    dbc = DBConnector(key)
    data = dbc.grab_mapping_data()
    mc = MasterCrawler(key, data)
    mc.crawl()