import base64

from locust import HttpLocust, TaskSet, task, between
from random import randint, choice, getrandbits, expovariate
from faker import Faker

class UserBehavior(TaskSet):
    
    '''
    @task(10)
    def registered_user_ordering(self):

        base64string = base64.b64encode(('{}:{}'.format('user', 'password')).encode('utf-8'))
        catalogue_ids = ['3395a43e-2d88-40de-b95f-e00e1502085b', '510a0d7e-8e83-4193-b483-e27e09ddc34d', '808a2de1-1aaa-4c25-a9b9-6612e8f29a38', '819e1fbf-8b7e-4f6d-811f-693534916a8b', '837ab141-399e-4c1f-9abc-bace40296bac', 'a0a4f044-b040-410d-8ead-4de0446aec7e', 'd3588630-ad8e-49df-bbd7-3167f7efb246', 'zzz4f044-b040-410d-8ead-4de0446aec7e']
        item_id = choice(catalogue_ids)

        self.client.get("/index.html")

        headers_w_auth = {}
        headers_w_auth["Authorization"] = "Basic {}".format(base64string.decode('utf-8'))
        # headers_w_auth["md.sid"] = self.client.cookies
        # headers = {}
        # headers["md.sid"] = self.client.cookies
        
        self.client.get("/cart")
        response = self.client.get("/login", headers=headers_w_auth)
        print(response.text)
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.delete("/cart")
        self.client.get("/basket.html")
        self.client.get("/address")
        self.client.get("/card")
        self.client.post("/orders")
        if bool(getrandbits(1)):
                self.client.get("/orders")
    
    '''
    @task(20)
    def registered_user_order_info(self):
        # self.client.cookies.clear()
        base64string = base64.b64encode(('{}:{}'.format('user', 'password')).encode('utf-8'))
        print("1")
        print(self.client.cookies)
        self.client.get("/index.html")
        print("2")
        print(self.client.cookies)
        self.client.get("/cart")
        print("3")
        print(self.client.cookies)
        headers = {}
        headers["Authorization"] = "Basic {}".format(base64string.decode('utf-8'))
        # headers["cookie"] = self.client.cookies["md.sid"]
        # print(headers)
        response = self.client.get("/login", headers=headers)
        print("4")
        print(self.client.cookies)
        self.client.close()
        print("5")
        print(self.client.cookies)
        
    

'''
class Web(HttpLocust):
    task_set = WebTasks
    min_wait = 0
    max_wait = 0
    wait_time = between(3, 8)
'''

class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    wait_time = lambda self: expovariate(1)
    task_set = UserBehavior
'''
def strictExp(min_wait,max_wait,mu=1):
    """
    Returns an exponentially distributed time strictly between two bounds.
    """
    while True:
        x = expovariate(mu)
        increment = (max_wait-min_wait)/(mu*6.0)
        result = min_wait + (x*increment)
        if result<max_wait:
            break
    return result

class StrictWebsiteUser(HttpLocust):
    """
    Locust user class that makes exponential requests but strictly between two bounds.
    """
    wait_time = lambda self: strictExp(3, 7)
    registered_user_ordering = RegisteredUserOrdering
    user_loggingin_searhing = UserLoggingInSearching
    user_registering_ordering = UserRegisteringOrdering
    user_searching = UserSearching
    user_searching_adding_to_cart = UserSearchingAddingToCart
    registered_user_order_info = RegisteredUserOrderInfo
'''
