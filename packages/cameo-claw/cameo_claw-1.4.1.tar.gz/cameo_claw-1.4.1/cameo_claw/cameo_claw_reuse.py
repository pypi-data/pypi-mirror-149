import gzip
from io import BytesIO
import polars as pl
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from cameo_claw.file import mkdir
from cameo_claw.net import url_to_filename, requests_get_ram_cache

import warnings
# import pandas as pd
from cameo_claw.functional import it_mp_f

warnings.filterwarnings("ignore")


def bytesio_to_gzip(df, url, target_directory):
    bytesio, filename = bytesio_filename(df, url)
    path = f'{target_directory}{filename}.csv.gz'
    write_gzip(bytesio, path)
    return url


def requests_get_write(f_write, target_directory, url):
    try:
        mkdir(target_directory)
        return requests_get_ram_cache(f_write, url, target_directory)
    except Exception as e:
        print(f'cameo_claw.py,requests_get_write,Exception:{e, url}')


def bytesio_filename(df, url, has_header=True):
    bytesio = BytesIO()
    df_write_csv(df, bytesio, has_header=has_header)
    filename = url_to_filename(url)
    return bytesio, filename


def df_write_csv(df, bytesio, has_header):
    '''
    fix polars bug
    polars has a bug, that iot attributes first byte lack a double quote " like this:
    attributes,createTime,deviceId,lat,localTime,lon,sensorId,value
    [{""key"":""ValueRaw"",""value"":""88.7""},{""key"":""Status"",""value"":""0""},{""key"":""ValueSD"",""value"":""0""},{""key"":""CollectRate"",""value"":""100.0""},{""key"":""Valid"",""value"":""0""}]",2022-04-21 00:02:00.042,11647957860,23.8549,2022-04-21 00:01:00.000,120.2696,rh,88.7
    "[{""key"":""ValueRaw"",""value"":""27""},{""key"":""Status"",""value"":""64""},{""key"":""ValueSD"",""value"":""0""},{""key"":""CollectRate"",""value"":""0.0""},{""key"":""Valid"",""value"":""4""}]",2022-04-21 00:02:00.042,11647957860,23.8549,2022-04-21 00:01:00.000,120.2696,pm2_5,27.0
    '''
    if df.row(0)[0][0] == '[':
        bytesio.write(b'"')
    return df.write_csv(bytesio, has_header=has_header)


def write_gzip(bytesio, path, mode='wb'):
    with gzip.open(path, mode) as f:
        f.write(bytesio.getvalue())
    return True


def pl_read_csv_distinct(bytes1, lst_distinct_column):
    df = pl.read_csv(bytes1, infer_schema_length=20000)
    df = df.distinct(subset=lst_distinct_column)
    return df


def pl_read_csv_str(bytes1):
    return pl.read_csv(bytes1, infer_schema_length=0).with_columns(pl.all().cast(pl.Int32, strict=False))


# def pd_read_csv(bytes1):
#     df = None
#     if bytes1[0:2] == b'\x1f\x8b':
#         df = pd.read_csv(BytesIO(bytes1), compression='gzip')
#     else:
#         df = pd.read_csv(BytesIO(bytes1))
#     return df


def groupby_write_gzip(df, url, lst_group_by_column, target_directory, has_header=True):
    for df in df.groupby(lst_group_by_column):
        df_write_gzip(df, has_header, lst_group_by_column, target_directory, url)
    return url


def df_write_gzip(df, has_header, lst_group_by_column, target_directory, url):
    filename_tail = '_group_' + '-'.join(list(
        map(lambda column:
            str(df.row(0)[df.find_idx_by_name(column)]).replace('_', '-'),
            lst_group_by_column)))
    bytesio, filename = bytesio_filename(df, url, has_header)
    path = f'{target_directory}{filename}{filename_tail}.csv.gz'
    write_gzip(bytesio, path)
    return filename_tail


def it_f(f, lst_url, target_directory, lst_distinct_column, lst_column_match, sort_column):
    return it_mp_f(f, [tuple([url, target_directory, lst_distinct_column,
                              lst_column_match, sort_column]) for url in lst_url])


def condition_filter_sort(df, lst_column_match, sort_column):
    df = df.filter(eval(condition(lst_column_match)))
    if sort_column:
        df = df.sort(sort_column)
    return df


def condition(lst_column_match):
    c = ''
    for lst_col_val in lst_column_match:
        c += f"""(pl.col('{lst_col_val[0]}')=='{lst_col_val[1]}') | """
    c = c[:-3]
    return c


def distinct_filter_sort(bytes1, lst_distinct_column, lst_column_match, sort_column):
    df = pl_read_csv_distinct(bytes1, lst_distinct_column)
    df = condition_filter_sort(df, lst_column_match, sort_column)
    return df


from fastapi.middleware.gzip import GZipMiddleware


def fastapi_app():
    app = FastAPI(docs_url="/d", redoc_url=None, openapi_url="/o.json")
    app.add_middleware(CORSMiddleware,
                       allow_origins=['*'],
                       allow_credentials=True,
                       allow_methods=['*'],
                       allow_headers=['*'])
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    return app


lst_demo_url = [
    'https://cameo-claw-data.vercel.app/device_21152332479_daily_2022-03-30.csv',
    'https://cameo-claw-data.vercel.app/device_21152332479_daily_2022-03-31.csv']


# 2022-04-21 bowen, copy from https://appdividend.com/2021/06/15/how-to-split-list-in-python/
def split_list(lst, n):
    yield from [lst[i: n + i] for i in range(0, len(lst), n)]
