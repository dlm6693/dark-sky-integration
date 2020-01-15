import json
import pandas as pd
import datetime
import os

#load fetched data
files = os.listdir()
jsons = [item for item in files if '.json' in item`]
last_json = max(json, key=os.path.getctime)
with open(last_json, encoding='utf-8') as f:
    data = json.load(f)

#change to list of dicts    
data_dict = [json.loads(item) for item in data]

#transforming hourly data
hourly_data = []
for item in data_dict:
    lat = item['latitude']
    lng = item['longitude']
    hourly_stats = item['hourly']['data']
    for v in hourly_stats:
        v.update({'latitude':lat, 'longitude':lng})
    hourly_data.append(hourly_stats)
hourly_data_list = [pd.DataFrame(item) for item in hourly_data]
hourly_data_df = pd.concat(hourly_data_list)

def update_and_transform(data_type,data_dict):
    refined_data = []
    for item in data_dict:
        lat = item['latitude']
        lng = item['longitude']
        if data_type in ['alerts', 'ALERTS', 'Alerts', 'alert', 'ALERT']:
            data = item['alerts']
        elif data_type in ['hourly', 'Hourly', 'HOURLY']:
            data = item['hourly']['data']
        elif data_type in ['daily', 'DAILY', 'Daily']:
            data = item['daily']['data']
        else:
            raise Exception('Unrecognized data section passed')
        for v in data:
            v.update({'lattitude':lat, 'longitude':lng})
        refined_data.append(data)
    df_list = [pd.DataFrame(item) for item in refined_data]
    return pd.concat(df_list)

update_and_transform(data_type='alerts', data_dict=data_dict)
update_and_transform(data_type='daily', data_dict=data_dict)
update_and_transform(data_type='hourly', data_dict=data_dict)
        