from datetime import date, datetime
import json
import os
import pprint
from random import random
import urllib.request
from http import cookiejar
from urllib.parse import urlencode
from pip._vendor import requests

credentials = {'login': 'mareks', 'password': 'mareks', "remember": "225200"}

params = dict(cookies=dict(), allow_redirects=False)
r = requests.post("http://localhost/login_handler", data=credentials, **params)


params["cookies"] = r.cookies
params["allow_redirects"] = True
params["headers"] = {'Content-Type': 'application/json'}

url = "http://localhost/api/v1/quick-key/tag/93fdc7b3-cd94-4d38-905e-221cf4c9406A"
# r = requests.get(url, **params)
# print(json.dumps(r.json(), indent=2))

tag = {
    "name": "grocery",
    "type": "EXPENSE",
}

r = requests.put(url, data=json.dumps(tag), **params)
print(r.text)

