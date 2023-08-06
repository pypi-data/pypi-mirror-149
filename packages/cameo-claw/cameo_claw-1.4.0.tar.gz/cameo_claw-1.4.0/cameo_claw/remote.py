from io import BytesIO
from time import sleep
from random import randint

from cameo_claw.net import requests_get_bytes
import polars as pl
import cameo_claw as cc


def square(x, dic={}):
    sleep(randint(0, 50))
    return {'square': x ** 2,
            'bytes': b'bytes \x00\x01\x02\x03 return 123'}


def df_hourly_time(df):
    df = df.with_column(pl.col("localTime").str.slice(0, 13).alias("hourly_time"))
    return df


def hourly_mean(url, d={}):
    try:
        bytes1 = requests_get_bytes(url)
        df = pl.read_csv(bytes1)
        df = cc.distinct(df, d['lst_distinct_column'])
        df = cc.filter(df, d['lst_column_match'])
        df = cc.sort(df, d['sort_column'])
        df = df_hourly_time(df)
        q = (df.lazy()
             .groupby(["hourly_time", "deviceId", "sensorId"])
             .agg([pl.first("lat"),
                   pl.first("lon"),
                   pl.col("value").mean()]))
        df = q.collect()
        bytesio = BytesIO()
        df.write_csv(bytesio)
        return {'is_success': True, 'url': url, 'csv': bytesio.getvalue().decode('utf-8')}
    except Exception as e:
        return {'is_success': False, 'url': url, 'exception': e}

