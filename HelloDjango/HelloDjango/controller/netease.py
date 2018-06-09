from django.http import HttpResponse
from django.shortcuts import render
from types import FunctionType
from django.views.decorators.csrf import csrf_exempt
from ..core import RouteConfig
from ..core import Router
from ..core import utils
from ..core.Common import AjaxResponse
import sys
import time
import datetime
import hashlib

class AppRoute:  # 定义控制类  方法名对应请求的 最后 uri
    def toAppSecretCreator(self , request):
        print()
        context = {}
        return render(request, 'netease/appSecretCreator.html', context)

    #获取签名
    def getAppkeySignature(self , request):
        print()
        reqParams = Router.getPostReqParams(request.POST);
        appSecret = reqParams['appSecret'];
        appkey = reqParams['appkey'];
        nonce = reqParams['nonce'];
        context = {}
        ajaxResp = AjaxResponse();
        ajaxResp.success = False;
        ajaxResp.msg = "操作成功";
        ajaxResp.result = {};
        myTime = time.time()
        timestamp = int(round(myTime * 1000));
        ajaxResp.result['timestamp'] = str(timestamp);
        ajaxResp.result['appkey'] = appkey;
        ajaxResp.result['nonce'] = nonce;
        timestamp = str(timestamp);
        ajaxResp.result['signature'] = getCheckSum(appSecret , nonce , timestamp);
        return Router.endAjaxHttpResponse(ajaxResp);



def getCheckSum(appSecret , nonce , timestamp):
    value = appSecret + nonce + timestamp;
    value = str(value);
    sha = hashlib.sha1(value.encode("utf8"))
    encrypts = sha.hexdigest()
    return encrypts;




# 初始化 路由类
appRouteInst  = AppRoute();

'''
处理请求转发， 通过 Router.route 方法 将请求映射到 AppRoute 的实例 （appRouteInst） 方法中处理
'''
@csrf_exempt
def route(request):
    return Router.route(request , utils.getThisPythonFileName(sys._getframe()) , AppRoute ,route , appRouteInst );




