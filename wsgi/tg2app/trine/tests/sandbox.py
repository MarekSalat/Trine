import os
import urllib.request
from http import cookiejar
from urllib.parse import urlencode
from pip._vendor import requests

jar = cookiejar.MozillaCookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0')]

# req = opener.open('http://localhost:8080/login?came_from=%2F')

credentials = {'login': 'mareks', 'password': 'mareks', "remember": 1}
# credenc = urlencode(credentials)
# binary_data = credenc.encode('utf-8')
#
# request = urllib.request.Request(
#     "http://localhost/api/v1/quick-key/fund.json", binary_data, auth=("mareks", "mareks"))
# request.get_method = lambda: 'POST'
# req = opener.open(request)
#
# print(req.headers)
#
# print(req.read())
# for cookie in jar:
#     print('%s : %s'%(cookie.name,cookie.value))
#     if cookie.name == "webflash":
#         val = urllib.parse.unquote(cookie.value)
#         val = urllib.parse.unquote(val)
#         print(val)

# opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
# urllib.request.install_opener(opener)
# req = opener.open('http://localhost:8080/api/v1/quick-key/fund.json')
# print(req.read())

cookies = dict(authtkt="c98434e3bf2311012d1e481d12ac6f4a53439e68mareks!")
# r = requests.post("http://localhost/login_handler", data=credentials, cookies=cookies, allow_redirects=True)
# print(r.cookies)
# print(r.status_code)
# print(r.history)

r = requests.get("http://localhost/api/v1/quick-key/fund.json", cookies=cookies, allow_redirects=True)
print(r.cookies)
print(r.status_code)
print(r.history)
print(r.json())

