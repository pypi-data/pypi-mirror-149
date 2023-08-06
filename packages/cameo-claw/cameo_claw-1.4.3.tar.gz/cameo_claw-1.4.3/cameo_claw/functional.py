from multiprocessing.dummy import Pool
from tqdm import tqdm
import cameo_claw.istarmap
from filelock import FileLock

cameo_claw.istarmap.ignore_no_use_warning()


def it_mp_f(f, tup_param, is_lock=True):
    if is_lock:
        # 2022-04-16 Bowen, 6 users query 3100 urls at the same time crashed, add FileLock to prevent it.
        with FileLock("it_mp_f.lock", timeout=60 * 60 * 2):
            yield from thread_pool_f(f, tup_param)
    else:
        yield from thread_pool_f(f, tup_param)


def thread_pool_f(f, tup_param):
    # 2022-04-10 bowen
    # fastapi + multiprocessing can crash, please use spawn to prevent it
    # https://miketarpey.medium.com/troubleshooting-usage-of-pythons-multiprocessing-module-in-a-fastapi-app-f1c368673686
    # it also fails!
    # finally, we use: from multiprocessing.dummy import Pool. Success!
    int_progress = 0
    with Pool(20) as p:
        for result in tqdm(p.istarmap(f, tup_param), total=len(tup_param)):
            int_progress += 1
            yield int_progress, result
