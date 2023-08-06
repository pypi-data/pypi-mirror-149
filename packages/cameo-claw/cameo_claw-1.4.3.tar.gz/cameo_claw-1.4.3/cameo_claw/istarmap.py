import multiprocessing.pool as mpp
import sys


def istarmap37(self, func, iterable, chunksize=1):
    """starmap-version of imap
    """
    if self._state != mpp.RUN:
        raise ValueError("Pool not running")
    task_batches = get_tasks(chunksize, func, iterable)
    result = mpp.IMapIterator(self._cache)
    return taskqueue_put(result, self, task_batches)


def taskqueue_put(result, self, task_batches):
    self._taskqueue.put(
        (
            self._guarded_task_generation(result._job,
                                          mpp.starmapstar,
                                          task_batches),
            result._set_length
        ))
    return (item for chunk in result for item in chunk)


def get_tasks(chunksize, func, iterable):
    if chunksize < 1:
        raise ValueError(
            "Chunksize must be 1+, not {0:n}".format(
                chunksize))
    task_batches = mpp.Pool._get_tasks(func, iterable, chunksize)
    return task_batches


def istarmap38(self, func, iterable, chunksize=1):
    """starmap-version of imap
    """
    self._check_running()
    task_batches = get_tasks(chunksize, func, iterable)
    result = mpp.IMapIterator(self)
    return taskqueue_put(result, self, task_batches)


if sys.version_info.major == 3 and sys.version_info.minor >= 8:
    mpp.Pool.istarmap = istarmap38
else:
    mpp.Pool.istarmap = istarmap37


def ignore_no_use_warning():
    pass
