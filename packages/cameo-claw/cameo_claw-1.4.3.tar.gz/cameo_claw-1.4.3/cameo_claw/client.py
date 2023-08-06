import asyncio
import json

from cameo_claw.net import async_post, async_get_json, async_get_read
from cameo_claw.scheduler import ItemClientAddTask


class Client:
    def __init__(self, scheduler_url='https://localhost:8000/api/map/'):
        self.scheduler_url = scheduler_url

    async def map(self, f, lst, dic={}, int_chunk_size=10):
        i = ItemClientAddTask()
        i.module_name = f.__module__
        i.function_name = f.__name__
        i.lst_iter = lst
        i.int_chunk_size = int_chunk_size
        i.dic_param = dic
        task_id = await async_post(f'{self.scheduler_url}client_add_task/', i.json())
        lst_done_chunk = []
        lst_result = []
        while True:
            lst_partial = await async_get_json(f'{self.scheduler_url}client_get_done_task/?task_id={task_id}')
            if not lst_partial:
                await asyncio.sleep(1)
                continue
            for dic_done in lst_partial:
                lst_done_chunk.append(dic_done['int_chunk_order'])
                # todo 2022-05-05 需測量：因為把所有結果都要記錄在 lst_result 可能記憶體爆炸，也可能耗CPU
                #   response要轉json再轉eval, 或許也是一種耗用, 要測速與記憶體
                for str_lst_result in dic_done['lst_result']:
                    lst_result.append(eval(str_lst_result))
            if len(lst_done_chunk) >= (len(lst) / int_chunk_size):
                break
        return lst_result
