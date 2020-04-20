'''
	User logging in and looking at orders
'''
import requests, time, base64
from random import randint, choice, getrandbits, expovariate

base_url = 'http://35.187.110.64'
# Initialize session, so that cookies get shared
ses = requests.session()
# I need this post w/o body for getting session id (ses.cookies['md.sid'])
res = ses.post('{}/login'.format(base_url))
# sessionId = ses.cookies['md.sid']
print(ses.cookies)
res = ses.get('{}/index.html'.format(base_url))
base64string = base64.b64encode(('{}:{}'.format('user', 'password')).encode('utf-8'))
# ses.get('{}/cart'.format(base_url))
headers = {}
headers["Authorization"] = "Basic {}".format(base64string.decode('utf-8'))
res = ses.post('{}/login'.format(base_url), headers=headers)
ses.get('{}/orders'.format(base_url))