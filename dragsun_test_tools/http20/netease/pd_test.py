# http请求模板
from hyper import HTTPConnection
import json


d = {
	"id" : 2051,
	"name" : "我是需求项目 333333333333" ,
	"purpose" : "我是需求项目目 333333333333" ,
	"description" : "我是描述 333333333333" ,
	"industryType" : 1 ,
	"workPlace" : "333333333333" ,
	"targetUser" : "目标客户哈哈哈 333333333333" ,
	"budget" : 32 ,
	"consumerId" : 1 ,
	"gmtPublish" : "2018-08-26 08:22:22" ,
	"attachUrlList" : "1,2,3,4" ,
	"arTemplateType" : 1 ,
	"arAppearType" : 3 ,
	"shareType" : 4 ,
	"couponType" : 5 ,
	"planCaseType" : 6 ,
	"pdConsumerId" : 1
};

params = json.dumps(d , ensure_ascii=False );
conn = HTTPConnection('localhost' , 11111)
conn.request('POST' , '/api/projects' , params , None)
resp = conn.get_response()
print(resp.read())


