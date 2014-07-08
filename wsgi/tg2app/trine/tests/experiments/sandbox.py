import json
import requests


params = dict(cookies=dict(), allow_redirects=False)
r = requests.post("http://localhost/login_handler?login=mareks&password=mareks", **params)

params["cookies"] = r.cookies
params["allow_redirects"] = True
params["headers"] = {'Content-Type': 'application/json'}

url = "http://localhost/api/v1/quick-key/tag"
r = requests.get(url, **params)
print(r.text)
print(params)

# tag = {
# "name": "grocery",
#     "type": "EXPENSE",
# }
#
# r = requests.put(url, data=json.dumps(tag), **params)
# print(r.text)

