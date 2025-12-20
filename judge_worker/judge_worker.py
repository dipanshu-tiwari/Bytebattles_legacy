import redis
import json
from .execute import execute

queue_task = 'task_queue'
queue_result = 'result_queue'

server = {
    'host': 'localhost',
    'port': 5431,
    'db': 0
}

def main():
    try:
        try:
            queue = redis.Redis(**server)
        except redis.exceptions.ConnectionError:
            print("[REDIS ERROR]: can\'t connect to redis")
            return
        
        print("[INFO]: worker started and running")
            
        running: bool = True
        while running:
            try:
                raw = queue.brpop(queue_task, timeout=0)
                
                if raw is None:
                    continue

                _, value = raw
                task = json.loads(value)

                print(f"[RECIEVED TASK]: {task['sid']}")

                result = execute(task)
                print(f"[RESULT RECIEVED]: {task['sid']}")
                queue.lpush(queue_result, json.dumps(result))
                
                print(f"[FINISHED TASK]: {task['sid']}")
            except Exception as e:
                print(f"[TASK ERROR]: unexpected error \"{e}\"")
                running = False

    except KeyboardInterrupt:
        print(f"Stoping Redis Queue (Keyboard Interrupt)")
    except Exception as e:
        print(f"[REDIS ERROR]: unexpected error \"{e}\"")
        return
    
main()