'''
	User browsing, adding to cart, registering and ordering
'''
import requests, time
from random import randint, choice, getrandbits, expovariate
from faker import Faker

base_url = 'http://35.187.110.64'
# Initialize session, so that cookies get shared
ses = requests.session()
# I need this post w/o body for getting session id (ses.cookies['md.sid'])
res = ses.post('{}/login'.format(base_url))
# sessionId = ses.cookies['md.sid']
print(ses.cookies)
res = ses.get('{}/index.html'.format(base_url))
catalogue_ids = ['03fef6ac-1896-4ce8-bd69-b798f85c6e0b', '3395a43e-2d88-40de-b95f-e00e1502085b', '510a0d7e-8e83-4193-b483-e27e09ddc34d', '808a2de1-1aaa-4c25-a9b9-6612e8f29a38', '819e1fbf-8b7e-4f6d-811f-693534916a8b', '837ab141-399e-4c1f-9abc-bace40296bac', 'a0a4f044-b040-410d-8ead-4de0446aec7e', 'd3588630-ad8e-49df-bbd7-3167f7efb246', 'zzz4f044-b040-410d-8ead-4de0446aec7e']
print(ses.cookies)
time.sleep(randint(3, 10))
ses.get('{}/cart'.format(base_url))
for i in range(0, randint(1, 5)):
	item_id = choice(catalogue_ids)
	ses.get('{}/category.html'.format(base_url))
	ses.get('{}/detail.html?id={}'.format(base_url, item_id))

for i in range(0, randint(1, 5)):
	item_id = choice(catalogue_ids)
	ses.get('{}/category.html'.format(base_url))
	ses.get('{}/detail.html?id={}'.format(base_url, item_id))
	if bool(getrandbits(1)):
		ses.post('{}/cart'.format(base_url), json={"id": item_id, "quantity": 1})
		ses.delete('{}/cart'.format(base_url))
faker = Faker()
firstname = faker.first_name()
lastname = faker.last_name()
password = faker.word()
email = faker.email()
ses.post('{}/register'.format(base_url), json={"username": firstname, "password": password, "email": email, "firstname": firstname, "lastname": lastname})
ses.get('{}/basket.html'.format(base_url))
ses.get('{}/address'.format(base_url))
ses.get('{}/card'.format(base_url))
ses.post('{}/addresses'.format(base_url), json={"number":"1","street":"Musterstreet","city":"Mustercity","postcode":"1234567","country":"Musterland"})
ses.post('{}/cards'.format(base_url), json={"longNum":"12345678","expires":"01/25","ccv":"987"})
ses.post('{}/orders'.format(base_url))