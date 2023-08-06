import httpx
import asyncio
import sys

from cameo_claw.net import async_post
from .cameo_claw import pipe
from datetime import datetime
from .scheduler import ItemWorkerDoneTask


async def worker_get_task(api_prefix):
    async with httpx.AsyncClient() as c:
        j = (await c.get(f'{api_prefix}worker_get_task/')).json()
        # print('debug worker_get_task j ', j)
        return j


async def do_task(d):
    """
    :param d: {
        'module_name': 'cameo_claw.remote',
        'function_name': 'square',
        'lst_iter': [30, 31],
        'int_chunk_size': 10,
        'dic_param': {},
        'task_id': '3ed384e8-b24a-4c9b-ab37-c420eb100d64',
        'int_chunk_order': 3,
        'date_time': '2022-04-23T14:10:35.915036'}
    :return:
    """
    if not d:
        return
    __import__(d['module_name'])
    f = getattr(sys.modules[d['module_name']], d['function_name'])
    return [r for i, r in pipe(f, d['lst_iter'], d['dic_param'], is_lock=False)]


async def worker_done_task(task_id, date_time, int_chunk_order, lst_result, api_prefix):
    """
    {
      "task_id": "b266e1ff-fd96-4753-bebc-c944693c8a92",
      "date_time": "2022-04-23T16:51:04.657299",
      "int_chunk_order": 0,
      "lst_result": [
        0,
        2,
        4
      ]
    }
    """
    i = ItemWorkerDoneTask()
    i.task_id = task_id
    i.date_time = date_time
    i.int_chunk_order = int_chunk_order
    # @@ todo debug, 若空的資料需要判斷，現在只是全部轉字串 isinstance(ValueError(),BaseException)
    i.lst_result = [str(s) for s in lst_result]
    # print('debug 🍎 worker.py i', i)
    # print('debug 🍊 worker.py i.json()', i.json())
    try:
        # @@ todo debug 這邊會因為 i.json() 包含 exception 結果掛掉
        # {'is_success': False, 'url': 'https://iot.epa.gov.tw/fapi_open/topic-device-daily/topic_save.industry.rawdata.material/device_10184237251/device_10184237251_daily_2022-03-06.csv.gz', 'exception': ValueError('Empty bytes data provided')},
        result = await async_post(f'{api_prefix}worker_done_task/', i.json())
        return result
    except Exception as e:
        print('worker.py worker_done_task exception:', e)
        print('worker.py worker_done_task i:', i)
        return False


async def loop_scheduler(api_prefix):
    while True:
        try:
            d = await worker_get_task(api_prefix)
            if not d:
                await asyncio.sleep(2)
                continue
            # 2022-04-24 Q: bowen 這邊有個疑惑是 f 並非 async
            #   所以會 block 一次只能跑 1 chunk task，這沒關係嗎？
            #   實際上是 await do_task, then pipe multithreading f 1_chunk 方式去跑的
            # @@ todo debug 這邊有可能發生錯誤要判斷，僅部分錯誤要能回傳部分正確
            #       這邊出錯最有可能是 https 連線 retry 連線錯誤，要在裡面處理才有機會部分回傳
            lst_result = await do_task(d)
            await worker_done_task(d['task_id'], datetime.now(), d['int_chunk_order'], lst_result, api_prefix)
        except Exception as e:
            print('worker.py loop_scheduler exception:', e)
            await asyncio.sleep(2)
            continue


async def main(api_url):
    lst_result = await asyncio.gather(loop_scheduler(api_url))


import sys

if __name__ == '__main__':
    print('debug worker.py start, api_url = sys.argv[1]')
    print('debug sh/worker.sh http://0.0.0.0:8000/')
    api_url = sys.argv[1]
    asyncio.run(main(api_url))
