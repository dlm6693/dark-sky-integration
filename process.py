import json
import pandas as pd
import datetime
import os
from Geohash import encode

#load fetched data
files = os.listdir()
jsons = [item for item in files if '.json' in item]
last_json = max(jsons, key=os.path.getctime)
with open(last_json, encoding='utf-8') as f:
    data = json.load(f)

#change to list of dicts    
data_dict = [json.loads(item) for item in data]
class DataProcessor(object):
    
    cols = ['geohash',
            'latitude',
            'longitude',
            'time']
    
    info_cols = ['icon',
                 'precipType',
                 'summary',
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
        'uvIndex',
        'visibility',
        'windBearing',
        'windGust',
        'windSpeed',
        ]
    
    daily_stats_cols = [
        'apparentTemperatureHigh',
        'apparentTemperatureHighTime',
        'apparentTemperatureLow',
        'apparentTemperatureLowTime',
        'apparentTemperatureMax',
        'apparentTemperatureMaxTime',
        'apparentTemperatureMin',
        'apparentTemperatureMinTime',
        'moonPhase',
        'precipIntensityMax',
        'precipIntensityMaxTime',
        'sunriseTime',
        'sunsetTime',
        'temperatureHigh',
        'temperatureHighTime',
        'temperatureLow',
        'temperatureLowTime',
        'temperatureMax',
        'temperatureMaxTime',
        'temperatureMin',
        'temperatureMinTime',
        'windGustTime',
    ]
    
    alerts_regions_cols = [
        'expires', 
        'regions',
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
        if 'precipType' and 'precipAccumulation' in df.columns:
            df = self.null_handler(df)
        time_cols = [col for col in daily.columns if 'time' in col.lower() or 'expires' in col.lower()]
        for col in time_cols:
            try:
                df[col] = pd.to_datetime(df[col], unit='s')
            except:
                continue
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df['geohash'] = df.apply(lambda x: encode(x['latitude'], x['longitude']), axis=1)
        return df.set_index('geohash')

    def null_handler(self, df):
        df['precipType'] = df['preciptype'].fillna(value='none')
        df['precipAccumulation'] = df['precipAccumulation'].fillna(value=0)
        return df
    
    def info_df(self, df):
        return df[cls.cols+cls.info_cols]
    
    def hourly_stats_df(self, df):
        return df[cls.cols+cls.stats_cols]
    
    def daily_stats_df(self, df):
        return df[cls.cols+cls.stats_cols+cls.daily_stats_cols]
    
    def alerts_regions_df(self, alerts_df):
        alerts_df['regions'] = alerts_df['regions'].map(lambda x:x.strip("]['").split(', '))
        regions = a
    
    
    
    
    
    
# alerts_df = update_and_transform(data_type='alerts', data_dict=data_dict)
# daily_df = update_and_transform(data_type='daily', data_dict=data_dict)
# hourly_df = update_and_transform(data_type='hourly', data_dict=data_dict)
# alerts_df.to_csv('alerts.csv', index=False)
# daily_df.to_csv('daily.csv', index=False)
# hourly_df.to_csv('hourly.csv', index=False)        