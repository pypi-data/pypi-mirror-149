import cameo_claw as cc


def pipe_download_iot_csv_gz(url, d):
    try:
        # print('debug worker_f.py pipe_download_iot_csv_gz d', d)
        df = cc.read_csv(url)
        df = cc.distinct(df, d['lst_distinct_column'])
        df = cc.filter(df, d['lst_column_match'])
        df = cc.sort(df, d['sort_column'])
        g = cc.groupby(df, d['lst_group_by_column'])
        for df in g:
            cc.to_csv_gz(df, d['target_directory'], url, d['lst_group_by_column'])
        return {'is_success': True, 'url': url}
    except Exception as e:
        return {'is_success': False, 'url': url, 'exception': e}
        #@@ todo debug 問題抓到了就在此，因為 e 無法 http post 回傳給 scheduler
