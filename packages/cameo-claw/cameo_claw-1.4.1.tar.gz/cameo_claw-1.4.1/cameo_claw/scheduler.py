from pydantic import BaseModel
from datetime import datetime
import uuid

from cameo_claw.cameo_claw_reuse import fastapi_app, split_list

app = fastapi_app()


class ItemClientAddTask(BaseModel):
    module_name: str = 'cameo_claw.remote'
    function_name: str = 'square'
    lst_iter: list = list(range(32))
    int_chunk_size: int = 10
    dic_param: dict = {}


lst_task_todo = []


class Task(ItemClientAddTask):
    task_id: str = None
    int_chunk_order: int = None
    date_time: datetime = None


@app.post("/api/client_add_task/")
async def client_add_task(i: ItemClientAddTask):
    task_id = uuid.uuid4()
    lst_chunk = split_list(i.lst_iter, i.int_chunk_size)
    for int_chunk_order, lst_iter in enumerate(lst_chunk):
        t = Task()
        t.task_id = task_id
        t.int_chunk_order = int_chunk_order
        t.date_time = datetime.now()
        t.module_name = i.module_name
        t.function_name = i.function_name
        t.lst_iter = lst_iter
        t.int_chunk_size = i.int_chunk_size
        t.dic_param = i.dic_param
        lst_task_todo.append(t)
    return task_id


@app.get("/api/dash_list_task/")
async def dash_list_task():
    return lst_task_todo


@app.get("/api/worker_get_task/")
async def worker_get_task():
    try:
        return lst_task_todo.pop(0)
    except Exception as e:
        return None


dic_done_task = {}


class ItemWorkerDoneTask(BaseModel):
    task_id: str = 'b266e1ff-fd96-4753-bebc-c944693c8a92'
    date_time: datetime = datetime.now()
    int_chunk_order: int = 0
    lst_result: list = [0, 2, 4]


@app.post("/api/worker_done_task/")
async def worker_done_task(i: ItemWorkerDoneTask):
    # print('debug worker_done_task', i)
    dic_done_task.setdefault(i.task_id, [])
    dic_done_task[i.task_id].append(i)
    return True


@app.get("/api/dash_list_done_task/")
async def dash_list_done_task(task_id):
    return dic_done_task.get(task_id, None)


@app.get("/api/client_get_done_task/")
async def client_get_done_task(task_id):
    return dic_done_task.pop(task_id, None)
