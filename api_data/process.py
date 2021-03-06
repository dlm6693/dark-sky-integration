import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json
import pandas as pd
import datetime
from Geohash import encode
from dark_sky_app import settings
from sqlalchemy import create_engine
from sqlalchemy.types import TIMESTAMP
import psycopg2
import uuid
import re

class DataProcessor(object):
    
    cols = [
        'id',
        'geohash',
        'latitude',
        'longitude',
        'time'
        ]
    
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
                data = item.get('alerts')
            elif data_type in ['hourly', 'Hourly', 'HOURLY']:
                data = item['hourly'].get('data')
            elif data_type in ['daily', 'DAILY', 'Daily']:
                data = item['daily'].get('data')
            else:
                raise Exception('Unrecognized data section passed')
            try:
                for v in data:
                    v.update({'latitude':lat, 'longitude':lng, 'tzone':tz})
            except:
                continue
            refined_data.append(data)
        df_list = [pd.DataFrame(item) for item in refined_data if item]
        if not df_list:
            return pd.DataFrame()
        df = pd.concat(df_list).reset_index(drop=True)
        df['id'] = [uuid.uuid4() for _ in range(len(df.index))]
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
        return df[self.cols+self.stats_cols+self.hourly_stats_cols]
    
    def daily_stats_df(self, df):
        return df[self.cols+self.stats_cols+self.daily_stats_cols]
    
    def alerts_regions_df(self, df):
        if df.empty:
            return df
        regions_df = df[self.cols+self.alerts_regions_cols]
        data = []
        for i,v in regions_df.iterrows():
            for lst in v['regions']:
                data_dict = {}
                data_dict['id'] = uuid.uuid4()
                data_dict['region'] = lst
                data_dict['time'] = v['time']
                data_dict['expires'] = v['expires']
                data_dict['latitude'] = v['latitude']
                data_dict['longitude'] = v['longitude']
                data_dict['geohash'] = v['geohash']
                data_dict['alert_id'] = v['id']
                data.append(data_dict)
        return pd.DataFrame(data)
    
    def alerts_df(self, df):
        if df.empty:
            return df
        return df[self.cols +self.alerts_cols]
    
    def process(self):
        alerts = self.update_and_transform('alerts')
        hourly = self.update_and_transform('hourly')
        daily = self.update_and_transform('daily')
        alertregions = self.alerts_regions_df(df=alerts)
        alerts = self.alerts_df(df=alerts)
        hourlyinfo = self.info_df(df=hourly)
        hourlystats = self.hourly_stats_df(df=hourly)
        dailyinfo = self.info_df(df=daily)
        dailystats = self.daily_stats_df(df=daily)
        df_dict = { 
            'api_data_alerts':alerts, 
            'api_data_alertregions':alertregions,
            'api_data_hourlyinfo':hourlyinfo, 
            'api_data_hourlystats':hourlystats, 
            'api_data_dailyinfo':dailyinfo, 
            'api_data_dailystats':dailystats
            }
        return df_dict
    
class DataIngestor(object):
    
    table_names = [
        'api_data_dailystats',
        'api_data_dailyinfo',
        'api_data_hourlystats',
        'api_data_hourlyinfo',
        'api_data_alertregions',
        'api_data_alerts',
    ]

    def __init__(self):
        
        user = settings.db_from_env['USER']
        password = settings.db_from_env['PASSWORD']
        database_name = settings.db_from_env['NAME']
        host = settings.db_from_env['HOST']
        port = settings.db_from_env['PORT']
        database_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}'
        self.conn = psycopg2.connect(dbname=database_name, user=user, host=host, password=password, port=port)
        self.engine = create_engine(database_url, echo=True)
        self.cursor = self.conn.cursor()
    
    def query_string_interpolation(self, df, columns):
        
        update_objects = [tuple(item) for index, item in df[columns].iterrows()]
        placeholders = []
        for item in update_objects:
            li_item = list(item)
            timestamps = [li_item[1]]
            if len(li_item) >= 3:
                ets = li_item[2]
                timestamps.append(ets)
            if all(isinstance(ts, pd.Timestamp) for ts in timestamps):
                sql_time_strings = [f"Timestamptz('{str(ts)}')" for ts in timestamps]
            else:
                raise Exception("Type of objects must be timestamp. Please reformat your data structure and try again.")
            new_item = [x for x in item if x not in timestamps]
            for idx, ts in enumerate(sql_time_strings):
                new_item.insert(idx+1, ts)
            placeholders.append(tuple(new_item))
        cleaned_col_string = str(columns).replace("[", "(").replace("]", ")").replace("'","")
        b_string = f"{cleaned_col_string} = "
        or_string = " ".join([f"{b_string}{str(x)} or" for x in placeholders])[:-3].replace('"',"")
        return or_string
    
    def ingest(self, df, table_name):
        
        if 'alertregions' in table_name:
            comp_cols = ['geohash', 'time', 'expires', 'region']
            update_cols = ['geohash', 'time', 'expires']
            str_cols = ", ".join(update_cols)
            update_or_string = self.query_string_interpolation(df, update_cols)
            update_query = f"SELECT id, {str_cols} FROM api_data_alerts WHERE {update_or_string}"
            alerts = pd.read_sql(con=self.engine,sql=update_query)
            for index, item in alerts.iterrows():
                idx_filter = df[(df['time'] == item['time']) & (df['geohash'] == item['geohash']) & (df['expires'] == item['expires'])].index
                df.loc[idx_filter, 'alert_id'] = item['id']
        elif 'alerts' in table_name:
            comp_cols = ['geohash', 'time', 'expires']
        else:
            comp_cols = ['geohash', 'time']
        df.drop_duplicates(subset=comp_cols, inplace=True)
        delete_or_string = self.query_string_interpolation(df, comp_cols)
        delete_query = f"DELETE FROM {table_name} WHERE id IN (SELECT id FROM {table_name} WHERE {delete_or_string})"
        self.cursor.execute(delete_query)
        self.conn.commit()
       
        time_cols = [col for col in df.columns if 'time' in col.lower() or 'expires' in col.lower()]
        conv_dict = {col:TIMESTAMP(timezone=True) for col in time_cols}
        df.to_sql(name=table_name, con=self.engine, if_exists='append', index=False, dtype=conv_dict, chunksize=1000)
    
    def basic_ingest(self, df, table_name):
        df.to_sql(name=table_name, con=self.engine, if_exists='append', index=False, chunksize=1000)
            
    def dispose_and_close(self):
        self.conn.close()
        self.engine.dispose()
