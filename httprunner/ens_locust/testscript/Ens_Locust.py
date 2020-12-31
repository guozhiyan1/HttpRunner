import random
from locust import TaskSet, task
from locust.events import request_failure
from httprunner.exceptions import MyBaseError, MyBaseFailure
from httprunner.ext.locusts.utils import prepare_locust_tests
from httprunner.runner import Runner
from locust import HttpLocust
import logging
logging.getLogger().setLevel(logging.ERROR)  # < - - - 默认为ERROR的很多信息都看不到看不到，建议调试设置为DEBUG
logging.getLogger('locust.main').setLevel(logging.INFO)
logging.getLogger('locust.runners').setLevel(logging.INFO)

class WebPageTasks(TaskSet):
    def on_start(self):
        config = {}
        self.test_runner = Runner(config, self.client)
        self.locust.tests = prepare_locust_tests("ens_locust/testcase/testcase1.yml")
        self.test_dict = random.choice(self.locust.tests)

    def run_test(self):
        try:
            self.test_runner.run_test(self.test_dict)    # < - - - 执行测试
            print("User instance (%r) executing my_task" % self)
        except (AssertionError, MyBaseError, MyBaseFailure) as ex:
            request_failure.fire(
                request_type=self.test_runner.exception_request_type,
                name=self.test_runner.exception_name,
                response_time=0,
                exception=ex
            )

    def on_stop(self):
        pass

    @task
    def test_1(self):
        self.run_test()



class WebPageUser(HttpLocust):  # < - - - 定义一个类 这里继承主要是为了继承基础的配置
    host = ""
    task_set = WebPageTasks  # < - - - TaskSet class that defines the execution behaviour of this locust
    min_wait = 0  # < - - - Use wait_time instead. Minimum waiting time between the execution of locust tasks
    max_wait = 0
