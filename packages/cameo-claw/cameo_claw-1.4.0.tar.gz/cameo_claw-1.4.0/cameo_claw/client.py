import asyncio

from cameo_claw.net import async_post, async_get
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
        while True:
            lst_partial = await async_get(f'{self.scheduler_url}client_get_done_task/?task_id={task_id}')
            if not lst_partial:
                await asyncio.sleep(1)
                continue
            for dic_done in lst_partial:
                lst_done_chunk.append(dic_done['int_chunk_order'])
                print(f"""debug dic_done['int_chunk_order']:{dic_done['int_chunk_order']}""")
            if len(lst_done_chunk) >= (len(lst) / int_chunk_size):
                break
