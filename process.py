import json
import pandas as pd
import datetime
import os
from Geohash import encode
from dark_sky_app.dark_sky_app import settings
from sqlalchemy import create_engine
import psycopg2

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
        'cloudCover',
        'dewPoint',
        'humidity',
        'ozone',
        'precipAccumulation',
        'precipIntensity',
        'precipProbability',
        'pressure',
        'uvIndex',
        'visibility',
        'windBearing',
        'windGust',
        'windSpeed',
        ]
    
    hourly_stats_cols = [
        'apparentTemperature',
        'temperature',
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
    
    alerts_cols = [
        'title',
        'severity',
        'expires',
        'description',
        'uri',
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
            tz = item['timezone']
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
                v.update({'latitude':lat, 'longitude':lng, 'tzone':tz})
            refined_data.append(data)
        df_list = [pd.DataFrame(item) for item in refined_data]
        df = pd.concat(df_list).reset_index(drop=True)
        if 'precipType' and 'precipAccumulation' in df.columns:
            df = self.null_handler(df)
        time_cols = [col for col in df.columns if 'time' in col.lower() or 'expires' in col.lower()]
        for col in time_cols:
            df[col] = df.apply(lambda x: pd.Timestamp(x[col], unit='s', tz=x['tzone']).tz_convert(tz='UTC'), axis=1)
        df['geohash'] = df.apply(lambda x: encode(x['latitude'], x['longitude']), axis=1)
        return df
    
    def null_handler(self, df):
        df['precipType'] = df['precipType'].fillna(value='none')
        df['precipAccumulation'] = df['precipAccumulation'].fillna(value=0)
        return df
    
    def info_df(self, df):
        return df[self.cols+self.info_cols]
    
    def hourly_stats_df(self, df):
        return df[self.cols+self.stats_cols]
    
    def daily_stats_df(self, df):
        return df[self.cols+self.stats_cols+self.daily_stats_cols]
    
    def alerts_regions_df(self, df):
        # df['regions'] = df['regions'].map(lambda x:x.strip("]['").split(', '))
        regions_df = df[self.cols+self.alerts_regions_cols]
        data = []
        for i,v in regions_df.iterrows():
            for lst in v['regions']:
                data_dict = {}
                data_dict['region'] = lst
                data_dict['time'] = v['time']
                data_dict['expires'] = v['expires']
                data_dict['latitude'] = v['latitude']
                data_dict['longitude'] = v['longitude']
                data_dict['geohash'] = v['geohash']
                data.append(data_dict)
        return pd.DataFrame(data)
    
    def alerts_df(self, df):
        return df[self.cols +self.alerts_cols]
    
    
    
class DataIngestor(object):
    
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']
    host = settings.DATABASES['default']['HOST']
    port = settings.DATABASES['default']['PORT']
    database_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}'
    
    table_names = [
        'api_data_dailystats',
        'api_data_dailyinfo',
        'api_data_hourlystats',
        'api_data_hourlyinfo',
        'api_data_alertregions',
        'api_data_alerts',
    ]

    def __init__(self):
        self.conn = psycopg2(dbname=database_name, user=user, host=host, password=password, port=port)
        self.engine = create_engine(database_url, echo=True)
        
    def ingest(self, df, table_name):
        df.to_sql(name=table_name, con=self.engine, if_exists='replace', index=False)
    
    
    
# dp = DataProcessor(data=data)
# alerts = dp.update_and_transform(data_type='alerts')
# daily = dp.update_and_transform(data_type='daily')
# hourly = dp.update_and_transform(data_type='hourly')
# alerts_regions_df = dp.alerts_regions_df(df=alerts)
# alerts_df = dp.alerts_df(df=alerts)
# hourly_info_df = dp.info_df(df=hourly)
# hourly_stats_df = dp.hourly_stats_df(df=hourly)
# daily_info_df = dp.info_df(df=daily)
# daily_stats_df = dp.daily_stats_df(df=daily)
