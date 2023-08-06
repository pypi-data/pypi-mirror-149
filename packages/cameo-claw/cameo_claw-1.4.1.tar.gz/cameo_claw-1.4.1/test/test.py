import asyncio

import polars

import cameo_claw as cc
from cameo_claw import mkdir
from cameo_claw.client import Client
from cameo_claw.net import url_to_filename
from cameo_claw.worker_f import pipe_download_iot_csv_gz
import os

lst_device_id = [
    '10180507985',
    '10183804818',
    '10180935138',
    '10182362729',
    '10186915768',
    '10182765572',
    '10183643733',
    '10187817545',
    '10180711468',
    '10181888891',
    '10184237251',
    '10200376949',
    '10187714974',
    '10188959173',
    '10181133624',
    '10189875513',
    '10184780057',
    '10187536226',
    '10188542674',
    '10187616860',
    '10190212306',
    '10200485379',
    '10184404771',
    '10188107333',
    '10186524358',
    '10187942042',
    '10183163884',
    '10180654119',
    '10185092420',
    '10187452115',
    '10190000864',
    '10190479538',
    '10185579073',
    '10181983795',
    '10188844366',
    '10189360662',
    '10182995926',
    '10181055695',
    '10189089883',
    '10181464107',
    '10184979038',
    '10181258942',
    '10184871059',
    '10185137651',
    '10182074994',
    '10190374312',
    '10186752944',
    '10189461434',
    '10184589018',
    '10181395211',
    '10186372622',
    '10186223376',
    '10182118699',
    '10190513901',
    '10185716972',
    '10189779191',
    '10188219952',
    '10185390063',
    '10181621345',
    '10182567005',
    '10186123517',
    '10188652949',
    '10184615499',
    '10189289540',
    '10182827296',
    '10185414614',
    '10184032107',
    '10185295344',
    '10182603505',
    '10186080368',
    '10187340888',
    '10186497242',
    '10187268812',
    '10183739942',
    '10188795449',
    '10183269165',
    '10183435474',
    '10180884769',
    '10188098571',
    '10183378041',
    '10185861505',
    '10183938343',
    '10185920135',
    '10181700710',
    '10188450871',
    '10186643177',
    '10184128532',
    '10190122978',
    '10188364226',
    '10184373796',
    '10186871514',
    '10181510720',
    '10183091769',
    '10187195615',
    '10182493773',
    '10187012610',
    '10182273531',
    '10183554350',
    '10185613026',
    '10189170767',
]


def get_lst_path_taipei_100(directory='./data/topic_pipe_download/', ext='.csv.gz'):
    lst_path = []
    for device_id in lst_device_id:
        for i in range(1, 32):  # range(1, 32)
            day = f'2022-03-{i:02}'
            path = f'{directory}device_{device_id}_daily_{day}{ext}'
            lst_path.append(path)
    return lst_path


def get_lst_url_taipei_100():
    return get_lst_url_by_date(lst_device_id)


def get_lst_url_by_date(lst_device_id):
    lst_url = []
    for device_id in lst_device_id:
        for i in range(1, 32):  # range(1, 32)
            day = f'2022-03-{i:02}'
            url = f'https://iot.epa.gov.tw/fapi_open/topic-device-daily/topic_save.industry.rawdata.material/device_{device_id}/device_{device_id}_daily_{day}.csv.gz'
            lst_url.append(url)
    return lst_url


def pipe_download_iot_zip(url, d):
    try:
        df = cc.read_csv(url)
        df = cc.distinct(df, d['lst_distinct_column'])
        df = cc.filter(df, d['lst_column_match'])
        df = cc.sort(df, d['sort_column'])
        g = cc.groupby(df, d['lst_group_by_column'])
        for df in g:
            cc.append_csv(df, d)
        return {'is_success': True, 'url': url}
    except Exception as e:
        return {'is_success': False, 'url': url, 'exception': e}


def test_pipe_download_iot_zip():
    d = {'lst_url': get_lst_url_taipei_100(),
         'target_directory': './data/topic_download_iot_zip/',
         'lst_distinct_column': ['deviceId', 'localTime', 'sensorId'],
         'lst_column_match': [['sensorId', 'pm2_5'], ['sensorId', 'voc']],
         'sort_column': 'localTime',
         'lst_group_by_column': ['deviceId', 'sensorId'],
         'append_column': 'deviceId',
         'column_header': 'createTime,deviceId,lat,localTime,lon,sensorId,value\n'}
    if cc.has_zip_cache(d):
        zip_cache_path = cc.zip_cache_path(d)
        print('zip_cache_path existed:', zip_cache_path)
        return zip_cache_path
    for int_progress, dic_result in cc.pipe(pipe_download_iot_zip, d['lst_url'], d):
        if not dic_result['is_success']:
            print(f"test_epa_download, e: {dic_result['exception']}, url: {dic_result['url']}'")
    return cc.zip_cache(d)


def test_pipe_download_iot_csv_gz():
    d = {'lst_url': get_lst_url_taipei_100(),
         'target_directory': './data/topic_download_iot_csv_gz/',
         'lst_distinct_column': ['deviceId', 'localTime', 'sensorId'],
         'lst_column_match': [['sensorId', 'pm2_5'], ['sensorId', 'voc']],
         'sort_column': 'localTime',
         'lst_group_by_column': ['deviceId', 'sensorId']}
    for int_progress, dic_result in cc.pipe(pipe_download_iot_csv_gz, d['lst_url'], d):
        if not dic_result['is_success']:
            print(f"test_epa_download, e: {dic_result['exception']}, url: {dic_result['url']}'")


# def pipe_nation(url, d):
#     try:
#         df = cc.read_csv(url)
#         df = cc.distinct(df, d['lst_distinct_column'])
#         df = cc.filter(df, d['lst_column_match'])
#         df = cc.sort(df, d['sort_column'])
#         g = cc.groupby(df, d['lst_group_by_column'])
#         for df in g:
#             cc.to_csv_gz(df, d['target_directory'], url, d['lst_group_by_column'])
#         return {'is_success': True, 'url': url}
#     except Exception as e:
#         return {'is_success': False, 'url': url, 'exception': e}
#
#
# def test_nation():
#     d = {'lst_url': [
#         'https://iot.epa.gov.tw/fapi_open/topic-device-daily/topic_save.nation.rawdata.material/device_11647957860/device_11647957860_daily_2022-04-21.csv.gz'],
#         'target_directory': './data/topic_nation/',
#         'lst_distinct_column': ['deviceId', 'localTime', 'sensorId'],
#         'lst_column_match': [['sensorId', 'pm2_5'], ['sensorId', 'voc']],
#         'sort_column': 'localTime',
#         'lst_group_by_column': ['deviceId', 'sensorId']}
#     for int_progress, dic_result in cc.pipe(pipe_nation, d['lst_url'], d):
#         if not dic_result['is_success']:
#             print(f"test_nation, e: {dic_result['exception']}, url: {dic_result['url']}'")


def pipe_nation_zip(url, d):
    try:
        df = cc.read_csv(url)
        df = cc.distinct(df, d['lst_distinct_column'])
        df = cc.filter(df, d['lst_column_match'])
        df = cc.sort(df, d['sort_column'])
        g = cc.groupby(df, d['lst_group_by_column'])
        for df in g:
            cc.append_csv(df, d)
        cc.append_csv(df, d)
        return {'is_success': True, 'url': url}
    except Exception as e:
        return {'is_success': False, 'url': url, 'exception': e}


def test_nation_zip():
    d = {'lst_url': [
        'https://iot.epa.gov.tw/fapi_open/topic-device-daily/topic_save.nation.rawdata.material/device_10841800054/device_10841800054_daily_2022-04-22.csv.gz'],
        'target_directory': './data/topic_nation_zip/',
        'lst_distinct_column': ['deviceId', 'localTime', 'sensorId'],
        'lst_column_match': [['sensorId', 'pm2_5'], ['sensorId', 'voc']],
        'sort_column': 'localTime',
        'lst_group_by_column': ['deviceId', 'sensorId'],
        'append_column': 'deviceId',
        'column_header': 'attributes,createTime,deviceId,lat,localTime,lon,sensorId,value\n'}
    if cc.has_zip_cache(d):
        zip_cache_path = cc.zip_cache_path(d)
        print('zip_cache_path existed:', zip_cache_path)
        return zip_cache_path
    for int_progress, dic_result in cc.pipe(pipe_nation_zip, d['lst_url'], d):
        if not dic_result['is_success']:
            print(f"test_epa_download, e: {dic_result['exception']}, url: {dic_result['url']}'")
    return cc.zip_cache(d)


async def test_client(api_url):
    client = Client(api_url)
    d = {
        'target_directory': './data/topic_download_iot_csv_gz/',
        'lst_distinct_column': ['deviceId', 'localTime', 'sensorId'],
        'lst_column_match': [['sensorId', 'pm2_5'], ['sensorId', 'voc']],
        'sort_column': 'localTime',
        'lst_group_by_column': ['deviceId', 'sensorId']}
    lst_result = await client.map(pipe_download_iot_csv_gz, get_lst_url_taipei_100()[0:10], d, int_chunk_size=100)


def pipe_download(url, d):
    try:
        cc.a_download(url, d['target_directory'])
        return {'is_success': True, 'url': url}
    except Exception as e:
        return {'is_success': False, 'url': url, 'exception': e}


def test_pipe_download():
    d = {'lst_url': get_lst_url_taipei_100(),
         'target_directory': './data/topic_pipe_download/',
         }
    for int_progress, dic_result in cc.pipe(pipe_download, d['lst_url'], d):
        if not dic_result['is_success']:
            print(f"test_epa_download, e: {dic_result['exception']}, url: {dic_result['url']}'")


def pipe_local(path, d):
    try:
        df = polars.read_csv(path)
        df = cc.distinct(df, d['lst_distinct_column'])
        df = cc.filter(df, d['lst_column_match'])
        df = cc.sort(df, d['sort_column'])
        g = cc.groupby(df, d['lst_group_by_column'])
        for df in g:
            cc.to_csv_gz(df, d['target_directory'], path, d['lst_group_by_column'])
        return {'is_success': True, 'url': path}
    except Exception as e:
        return {'is_success': False, 'url': path, 'exception': e}


def test_local():
    d = {'target_directory': './data/topic_download_iot_csv_gz/',
         'lst_distinct_column': ['deviceId', 'localTime', 'sensorId'],
         'lst_column_match': [['sensorId', 'pm2_5'], ['sensorId', 'voc']],
         'sort_column': 'localTime',
         'lst_group_by_column': ['deviceId', 'sensorId']}
    for int_progress, dic_result in cc.pipe(pipe_local, get_lst_path_taipei_100(), d):
        if not dic_result['is_success']:
            print(f"test_epa_download, e: {dic_result['exception']}, url: {dic_result['url']}'")


def test_local_csv():
    d = {'target_directory': './data/topic_download_iot_csv_gz/',
         'lst_distinct_column': ['deviceId', 'localTime', 'sensorId'],
         'lst_column_match': [['sensorId', 'pm2_5'], ['sensorId', 'voc']],
         'sort_column': 'localTime',
         'lst_group_by_column': ['deviceId', 'sensorId']}
    for int_progress, dic_result in cc.pipe(pipe_local, get_lst_path_taipei_100('./data/topic_csv/', '.csv'), d):
        if not dic_result['is_success']:
            print(f"test_epa_download, e: {dic_result['exception']}, url: {dic_result['url']}'")


def pipe_local_csv_to_parquet(path, d):
    try:
        df = polars.read_csv(path)
        to_path = d['target_directory'] + url_to_filename(path, is_ext=False) + '.parquet'
        df.write_parquet(to_path, compression="snappy")
        return {'is_success': True, 'path': path}
    except Exception as e:
        return {'is_success': False, 'path': path, 'exception': e}


def test_local_csv_to_parquet():
    d = {'target_directory': './data/topic_parquet/'}
    mkdir('./data/topic_parquet/')
    for int_progress, dic_result in cc.pipe(pipe_local_csv_to_parquet,
                                            get_lst_path_taipei_100('./data/topic_csv/', '.csv'), d):
        if not dic_result['is_success']:
            print(f"test_epa_download, e: {dic_result['exception']}, path: {dic_result['path']}'")


def pipe_local_parquet_compute(path, d):
    try:
        df = polars.read_parquet(path)
        df = cc.distinct(df, d['lst_distinct_column'])
        df = cc.filter(df, d['lst_column_match'])
        df = cc.sort(df, d['sort_column'])
        g = cc.groupby(df, d['lst_group_by_column'])
        for df in g:
            cc.to_parquet(df, d['target_directory'], path, d['lst_group_by_column'])
            # cc.to_csv_gz(df, d['target_directory'], path, d['lst_group_by_column'])
        return {'is_success': True, 'path': path}
    except Exception as e:
        return {'is_success': False, 'path': path, 'exception': e}


def test_local_parquet_compute():
    d = {'target_directory': './data/topic_parquet_compute/',
         'lst_distinct_column': ['deviceId', 'localTime', 'sensorId'],
         'lst_column_match': [['sensorId', 'pm2_5'], ['sensorId', 'voc']],
         'sort_column': 'localTime',
         'lst_group_by_column': ['deviceId', 'sensorId']}
    mkdir('./data/topic_parquet_compute/')
    for int_progress, dic_result in cc.pipe(pipe_local_parquet_compute,
                                            get_lst_path_taipei_100('./data/topic_parquet/', '.parquet'), d):
        if not dic_result['is_success']:
            print(f"test_epa_download, e: {dic_result['exception']}, path: {dic_result['path']}'")


if __name__ == '__main__':
    # test_pipe_download_iot_zip()
    # test_pipe_download_iot_csv_gz()
    # test_nation_zip()
    # test_pipe_download() # 純下載無計算
    # test_local()
    # test_local_csv()
    # test_local_csv_to_parquet()
    # test_local_parquet_compute()
    asyncio.run(test_client('http://0.0.0.0:8000/api/'))
