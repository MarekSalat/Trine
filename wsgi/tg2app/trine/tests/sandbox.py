import json
import requests

credentials = {'login': 'mareks', 'password': 'mareks', "remember": "225200"}

params = dict(cookies=dict(), allow_redirects=False)
r = requests.post("http://localhost/login_handler", data=credentials, **params)


params["cookies"] = r.cookies
params["allow_redirects"] = True
params["headers"] = {'Content-Type': 'application/json'}

url = "http://localhost/api/v1/quick-key/tag"
r = requests.get(url, **params)
print(json.dumps(r.json(), indent=2))

# tag = {
#     "name": "tag " + str(random()),
# }
#
# r = requests.post(url, data=json.dumps(tag), **params)
# print(r.text)

