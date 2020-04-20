import base64

from locust import HttpLocust, TaskSet, task, between
from random import randint, choice, getrandbits, expovariate
from faker import Faker

class UserBehavior(TaskSet):
    @task(5)
    def user_registering_ordering(self):
        catalogue_ids = ['3395a43e-2d88-40de-b95f-e00e1502085b', '510a0d7e-8e83-4193-b483-e27e09ddc34d', '808a2de1-1aaa-4c25-a9b9-6612e8f29a38', '819e1fbf-8b7e-4f6d-811f-693534916a8b', '837ab141-399e-4c1f-9abc-bace40296bac', 'a0a4f044-b040-410d-8ead-4de0446aec7e', 'd3588630-ad8e-49df-bbd7-3167f7efb246', 'zzz4f044-b040-410d-8ead-4de0446aec7e']
        headers = {}
        headers["md.sid"] = self.client.cookies["md.sid"]
        self.client.get("/", headers=headers)
        self.client.get("/cart", headers=headers)
        for i in range(randint(1, 5), randint(1, 5)):
            item_id = choice(catalogue_ids)
            self.client.get("/category.html", headers=headers)
            self.client.get("/detail.html?id={}".format(item_id), headers=headers)
            if bool(getrandbits(1)):
                self.client.post("/cart", json={"id": item_id, "quantity": 1}, headers=headers)
                self.client.delete("/cart", headers=headers)
        faker = Faker()
        firstname = faker.first_name()
        lastname = faker.last_name()
        password = faker.word()
        email = faker.email()
        self.client.post("/register", json={"username": firstname, "password": password, "email": email, "firstname": firstname, "lastname": lastname}, headers=headers)
        self.client.get("/basket.html", headers=headers)
        self.client.get("/address", headers=headers)
        self.client.get("/card", headers=headers)
        self.client.post("/addresses", json={"number":"1","street":"Musterstreet","city":"Mustercity","postcode":"1234567","country":"Musterland"}, headers=headers)
        self.client.post("/cards", json={"longNum":"12345678","expires":"01/25","ccv":"987"}, headers=headers)
        self.client.post("/orders", headers=headers)

class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    wait_time = lambda self: expovariate(1)
    task_set = UserBehavior
