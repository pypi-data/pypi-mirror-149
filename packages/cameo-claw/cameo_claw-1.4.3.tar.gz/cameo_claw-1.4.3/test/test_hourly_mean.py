from cameo_claw.remote import hourly_mean


def test_hourly_mean():
    d = {}
    url = 'https://iot.epa.gov.tw/fapi_open/topic-device-daily/topic_save.industry.rawdata.material/device_11135655524/device_11135655524_daily_2022-03-31.csv.gz'
    d['lst_distinct_column'] = ['deviceId', 'localTime', 'sensorId']
    d['lst_column_match'] = [['sensorId', 'pm2_5'], ]
    d['sort_column'] = 'localTime'
    dic_result = hourly_mean(url, d)
    print(dic_result)
