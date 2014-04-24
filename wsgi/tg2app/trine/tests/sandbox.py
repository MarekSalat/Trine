from datetime import date, datetime
import json
import os
import pprint
import urllib.request
from http import cookiejar
from urllib.parse import urlencode
from pip._vendor import requests

credentials = {'login': 'mareks', 'password': 'mareks', "remember": "2252000"}

params = dict(cookies=dict(), allow_redirects=False)
r = requests.post("http://localhost/login_handler", data=credentials, **params)
params["cookies"] = r.cookies
params["allow_redirects"] = True
params["headers"] = {'Content-Type': 'application/json'}

url = "http://localhost/api/v1/quick-key/fund.json"
r = requests.get(url, **params)

print(json.dumps(r.json(), indent=2))

fund = {
    '_user_id': '5a66533f-3cdc-4a7b-9511-fce91da9a6cd',
    'amount': 942.0,
    'currency': 'EUR',
    'date': "2014-04-09 12:30:00",
    'description': None,
    'expenseTagGroup_id': None,
    'foreignCurrency': 1.42,
    'incomeTagGroup_id': 'dce85abb-b141-4b16-b87d-90f301aaface'
}

tag = {"name": "xxxx", "type": "EXPENSE", "_user_id": "d09b9111-70a0-43c0-9373-aba10f2af592", 'created': "2014-04-09 12:30:00",}

r = requests.post("http://localhost/admin/tags.json", data=json.dumps(tag), **params)
print(r.text)

