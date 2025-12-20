import json
import redis

from django.core.management.base import BaseCommand
from submissions.models import Submission  # adjust if needed

from judge.redis_config import server, queue_result


class Command(BaseCommand):
    help = "Background worker to consume results from Redis queue and store in DB"

    def handle(self, *args, **options):
        queue = redis.Redis(**server)

        print("[Result Worker] Listening for results...")

        try:
            while True:
                try:
                    _, data = queue.blpop(queue_result)  # blocks until item available

                    if data is None:
                        continue

                    result = json.loads(data)

                    print(f"[ResultWorker] Got result: {result}")

                    # Save result to DB
                    submission = Submission.objects.get(pk=result["sid"])
                    submission.verdict = result["verdict"]
                    submission.memory = result.get("maxMem")
                    submission.walltime = result.get("wallTime")
                    submission.incorrect_testcase = result.get("testcase")
                    submission.output = result.get("output")
                    submission.save()

                    problem = submission.problem
                    problem.total_submissions = problem.total_submissions + 1

                    if submission.verdict == "AC":
                        problem.accepted_submissions = problem.accepted_submissions + 1

                    problem.save()

                    print(f"[ResultWorker] Saved verdict for submission {submission.id}")
                except Exception as e:
                    print(f"[ERROR]: {e}")
        except KeyboardInterrupt:
            print("CLOSING THE WORKER")
        except Exception as e:
            print(f"[FATAL ERROR]: {e}")