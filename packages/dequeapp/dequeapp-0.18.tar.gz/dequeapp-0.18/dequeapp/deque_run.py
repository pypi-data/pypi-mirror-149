import datetime
import os
import subprocess

import coolname

from dequeapp.rest_connect import RestConnect
from dequeapp.deque_environment import AGENT_API_SERVICE_URL
from dequeapp.redis_services import RedisServices
import pickle
import multiprocessing
from dequeapp.parsing_service import ParsingService


def decode_datetime(obj):
    if '__datetime__' in obj:
        obj = datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
    return obj


def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    return obj

class Run:
    def __init__(self):
        self.user_name = None

        self._workload_type = None
        self._submission_id = None

        self.project_id = None

        self.params = dict()
        self._history = dict()
        self._step = 0
        self._rest = RestConnect()
        self._redis = RedisServices.get_redis_connection()




    def init(self, user_name=None, project_name=None):
        self.user_name = user_name

        if project_name is None:
            self.project_id = coolname.generate_slug(2)
        else:
            self.project_id = project_name

        self._submission_id = os.getenv("submission_id")
        self._workload_type = os.getenv("workload_type")
        if self._submission_id is None or self._workload_type is None:
            self._submission_id = "test_submission"
            self._workload_type = "notebook"
            # raise Exception("Experiment Tracking is only supported with Deque AI tools. Get yours at https://deque.app")
        print("starting redis")
        p1 = multiprocessing.Process(target=self.start_redis)
        p1.start()
        p2 = multiprocessing.Process(target=self.start_parser)
        p2.start()
        p1.join()
        p2.join()


        self._redis.sadd("submission_ids:", self._submission_id)

    def start_parser(self):
        parser = ParsingService()
        parser.receive()

    def start_redis(self):
        subprocess.Popen(["/opt/miniconda3/envs/deque/lib/python3.9/site-packages/redis_server/bin/redis-server"])
            #(["/home/supercompute/miniconda3/envs/dq_notebook_agent/lib/python3.8/site-packages/redis_server/bin/redis-server"])

    def send_data_to_redis(self, submission_id, step, data):


        key = "submission_id:step:data:" + self._submission_id + str(self._step)

        self._redis.sadd("submission_id:steps:" + submission_id, str(step))

        data_pickled = pickle.dumps(data)


        self._redis.set(key, data_pickled)


    def log(self, data, step=None, commit=True):
        data.update(
            {"user_name": self.user_name, "submission_id": self._submission_id, "workload_type": self._workload_type,
             "project_id": self.project_id, "deque_log_time": datetime.datetime.now(),"step":self._step})


        self.send_data_to_redis(submission_id=self._submission_id, step=self._step, data=data)
        if commit:
            self._step += 1




    def send_upstream(self):
        self._rest.post(url=AGENT_API_SERVICE_URL + "/fex/python/track/", json=self._history)
        self._history = dict()



if __name__ == "__main__":
    deque = Run()
    deque.init(user_name="riju@deque.app", project_name="awesome-dude")
    for i in range(100):
        deque.log(data={"train":{"accuracy": i,"loss":i-100},"image":deque.im})

    # deque.log(data={"image":deque.im})
