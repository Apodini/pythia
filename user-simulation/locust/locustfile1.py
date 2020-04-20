import base64, time, uuid

from locust import HttpLocust, TaskSet, task, between
from random import randint, choice, getrandbits, expovariate


class UserBehavior(TaskSet):
    
    @task(50)
    def user_searching(self):
        catalogue_ids = ['03fef6ac-1896-4ce8-bd69-b798f85c6e0b', '3395a43e-2d88-40de-b95f-e00e1502085b', '510a0d7e-8e83-4193-b483-e27e09ddc34d', '808a2de1-1aaa-4c25-a9b9-6612e8f29a38', '819e1fbf-8b7e-4f6d-811f-693534916a8b', '837ab141-399e-4c1f-9abc-bace40296bac', 'a0a4f044-b040-410d-8ead-4de0446aec7e', 'd3588630-ad8e-49df-bbd7-3167f7efb246', 'zzz4f044-b040-410d-8ead-4de0446aec7e']
        '''cookie = str(uuid.uuid4())
        headers = {}
        headers["md.sid"] = cookie'''
        print(self.client.cookies)
        self.client.post("/login")
        response = self.client.get("/index.html")
        print(self.client.cookies)
        time.sleep(3)
        self.client.get("/cart")
        for i in range(randint(1, 5), randint(1, 5)):
            item_id = choice(catalogue_ids)
            self.client.get("/category.html")
            self.client.get("/detail.html?id={}".format(item_id))

class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    wait_time = lambda self: expovariate(1)
    task_set = UserBehavior