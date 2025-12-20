import redis
import json
from .redis_config import server, queue_task

from submissions.models import Submission

def getTask(pk):
    submission = Submission.objects.get(pk=pk)
    task = {
        'sid': pk,
        'language': submission.language,
        'code': submission.code,
        'pid': submission.problem.pid,
        'memLimit': submission.problem.memory_limit,
        'timeLimit': submission.problem.time_limit,
        'testCount': submission.problem.test_count
    }

    return task

def enqueueTask(pk):
    task = getTask(pk)
    queue = redis.Redis(**server)
    queue.lpush(queue_task, json.dumps(task))