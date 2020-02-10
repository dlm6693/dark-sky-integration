def crawl():
    import pandas as pd
    import os
    from dark_sky_app import settings
    from api_data.master_crawler import MasterCrawler
    key_path = os.path.join(settings.BASE_DIR, 'api_data/secret_key.txt')
    with open(key_path, "r") as f:
        key = f.read()
    loc_data = pd.read_csv("api_data/uscities.csv")
    lat_long = loc_data[["lat", "lng"]][:10]
    mc = MasterCrawler(mapping_data = lat_long, key=key)
    mc.crawl()