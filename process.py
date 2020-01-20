import json
import pandas as pd
import datetime
import os

#load fetched data
files = os.listdir()
jsons = [item for item in files if '.json' in item]
last_json = max(jsons, key=os.path.getctime)
with open(last_json, encoding='utf-8') as f:
    data = json.load(f)

#change to list of dicts    
data_dict = [json.loads(item) for item in data]
class DataProcessor(object):
    
    info_cols = ['icon',
                 'precipType',
                 'summary', 
                 'time',
                 ]
    
    stats_cols = [
        'apparentTemperature',
        'cloudCover',
        'dewPoint',
        'humidity',
        'ozone',
        'precipAccumulation',
        'precipIntensity',
        'precipProbability',
        'pressure',
        'temperature',
        'time',
        'uvIndex',
        'visibility',
        'windBearing',
        'windGust',
        'windSpeed',
        ]
                    
    def __init__(self, data):
        self.data_dict = [json.loads(item) for item in data]
    
    def update_and_transform(self, data_type):
        refined_data = []
        for item in self.data_dict:
            lat = item['latitude']
            lng = item['longitude']
            if data_type in ['alerts', 'ALERTS', 'Alerts', 'alert', 'ALERT']:
                try:
                    data = item['alerts']
                except KeyError:
                    continue
            elif data_type in ['hourly', 'Hourly', 'HOURLY']:
                data = item['hourly']['data']
            elif data_type in ['daily', 'DAILY', 'Daily']:
                data = item['daily']['data']
            else:
                raise Exception('Unrecognized data section passed')
            for v in data:
                v.update({'latitude':lat, 'longitude':lng})
            refined_data.append(data)
        df_list = [pd.DataFrame(item) for item in refined_data]
        df = pd.concat(df_list)
        if 'precipType' and 'precipAccumulation' in hourly.columns:
            df = self.null_handler(df)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def null_handler(self, df):
        df['precipType'] = df['preciptype'].fillna(value='none')
        df['precipAccumulation'] = df['precipAccumulation'].fillna(value=0)
        return df
    
    def info_df(self, df):
        return df[cls.info_cols]
    
    def stats_df(self, df):
        return df[cls.stats_cols]
    
    
    
    
    
    
    
    
# alerts_df = update_and_transform(data_type='alerts', data_dict=data_dict)
# daily_df = update_and_transform(data_type='daily', data_dict=data_dict)
# hourly_df = update_and_transform(data_type='hourly', data_dict=data_dict)
# alerts_df.to_csv('alerts.csv', index=False)
# daily_df.to_csv('daily.csv', index=False)
# hourly_df.to_csv('hourly.csv', index=False)        