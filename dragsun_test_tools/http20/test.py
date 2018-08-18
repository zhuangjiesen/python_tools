# http请求模板
from hyper import HTTPConnection

print('hello ...');
# conn = HTTPConnection('static.meiqia.com',port=443,secure=True)
conn = HTTPConnection('login.netease.com',port=443,secure=True)
conn.request('GET' , '/connect/userinfo?access_token=19c6ace9d4244a51bf83294d1bdea44f')
# conn.request('GET' , '/dist/meiqia.js')
resp = conn.get_response()
# https://static.meiqia.com/dist/meiqia.js
# https://dongjian-api-dev.netease.com/
print(resp.read())