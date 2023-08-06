import gzip
from hashlib import md5
from io import BytesIO

import requests
import uvicorn
from fastapi.responses import StreamingResponse
from cameo_claw.cameo_claw import it_chunk_pl

from pydantic import BaseModel

from cameo_claw.cameo_claw_reuse import fastapi_app, lst_demo_url

app = fastapi_app()


class ItemUrlFilter(BaseModel):
    lst_url: list = lst_demo_url
    target_directory: str = './data/topic_filter/'
    lst_distinct_column: list = ['deviceId', 'localTime', 'sensorId']
    lst_column_match: list = [
        ['sensorId', 'pm2_5'],
        ['sensorId', 'voc']
    ]
    sort_column: str = 'localTime'


def it_streaming_pl(i: ItemUrlFilter):
    try:
        yield write_csv_header_to_gz_pl(i)
        for bytes1 in it_chunk_pl(
                i.lst_url, i.target_directory, i.lst_distinct_column, i.lst_column_match, i.sort_column):
            if bytes1:
                yield bytes1
            else:
                continue
    except Exception as e:
        print('it_streaming_pl,exception:', e)


# def write_csv_header_to_gz_pd(i):
#     r = requests.get(i.lst_url[0], verify=False)
#     df = pd_read_csv(r.content)
#     bytesio_gz = BytesIO()
#     with gzip.open(bytesio_gz, 'wb') as f:
#         f.write((','.join(df.columns) + '\n').encode('utf-8'))
#     return bytesio_gz.getvalue()


def write_csv_header_to_gz_pl(i):
    bytesio_gz = BytesIO()
    lst_column = ['createTime', 'deviceId', 'lat', 'localTime', 'lon', 'sensorId', 'value']
    with gzip.open(bytesio_gz, 'wb') as f:
        f.write((','.join(lst_column) + '\n').encode('utf-8'))
    return bytesio_gz.getvalue()


dic_item_url_filter = {}


@app.post("/api/streaming_post/")
def streaming_post(i: ItemUrlFilter):
    md5_hex = md5(str(i).encode()).hexdigest()
    dic_item_url_filter[md5_hex] = i
    return md5_hex


@app.get("/api/streaming_get_pl/")
def streaming_get_pl(md5_hex):
    dic = {'content-disposition': f"attachment; filename*=utf-8''all.csv.gz"}
    return StreamingResponse(it_streaming_pl(dic_item_url_filter[md5_hex]), headers=dic)


def server(host='0.0.0.0', int_port=20412):
    uvicorn.run("cameo_claw.streaming:app", host=host, port=int_port, reload=False, debug=False, workers=1)
